#!/usr/bin/env python3
"""Retrieve candidate plant papers; publish only explicitly reviewed decisions.

Runtime files live beside this script in data/. No credentials are required.
Review schema: {"decisions": [{"pmid": "123", "status": "include|exclude|pending",
"category": "spatial|time|spatial, time", "evidence": "...", "sources": ["https://..."]}]}.
Metadata may be supplied or overridden in a decision. Changes to an already
included record require "correction": true. This program never classifies papers.
"""
import argparse
from contextlib import contextmanager
import copy
import csv
import datetime as dt
import hashlib
import html
import io
import json
import os
from pathlib import Path
import re
import ssl
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

HOME = Path(__file__).resolve().parent
HEADERS = ["data_type", "year", "title", "PMID"]
CATEGORIES = {"spatial": "spatial", "time": "time", "spatialtime": "spatial, time",
              "spatial, time": "spatial, time", "spatial,time": "spatial, time"}


@contextmanager
def state_lock(directory):
    """Serialize local CLI and MCP writes (POSIX/macOS, advisory file lock)."""
    import fcntl
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".state.lock").open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def atomic_write(path, content):
    """Replace a file only after all bytes have been written and flushed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = content if isinstance(content, bytes) else content.encode("utf-8")
    fd, temporary = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save_json(path, value):
    atomic_write(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def normalize_doi(value):
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", str(value or "").strip(), flags=re.I).lower().rstrip(".")


def normalize_title(value):
    return re.sub(r"[^a-z0-9]", "", clean_title(value).lower())


def clean_title(value):
    return re.sub(r"<[^>]*>", "", html.unescape(str(value))).strip()


def has_sources(record):
    sources = record.get("sources", [])
    return isinstance(sources, list) and any(urlparse(str(url)).scheme in {"http", "https"}
                                            and urlparse(str(url)).netloc for url in sources)


def record_keys(record):
    keys = {"pmid:" + str(record["pmid"])}
    if normalize_doi(record.get("doi")):
        keys.add("doi:" + normalize_doi(record["doi"]))
    return keys


def deduplicate(records):
    """Collapse equal identities, refusing inconsistent PMID/DOI metadata."""
    result, by_key = [], {}
    for original in records:
        record = copy.deepcopy(original)
        keys = record_keys(record)
        matches = {by_key[key] for key in keys if key in by_key}
        if len(matches) > 1:
            raise ValueError("Conflicting PMID/DOI identity: " + record["pmid"])
        if matches:
            previous = result[next(iter(matches))]
            doia, doib = normalize_doi(previous.get("doi")), normalize_doi(record.get("doi"))
            if normalize_title(previous["title"]) != normalize_title(record["title"]) or (doia and doib and doia != doib):
                raise ValueError("Conflicting duplicate metadata: " + record["pmid"])
            for key in keys:
                by_key[key] = next(iter(matches))
            continue
        index = len(result)
        result.append(record)
        for key in keys:
            by_key[key] = index
    return result


def local_today(config):
    return dt.datetime.now(ZoneInfo(config["timezone"])).date()


def validate_include(record, config, today):
    record = copy.deepcopy(record)
    record["pmid"] = str(record.get("pmid", "")).strip()
    if not re.fullmatch(r"[1-9][0-9]*", record["pmid"]):
        raise ValueError("Include requires a numeric PMID")
    record["title"] = clean_title(record.get("title", ""))
    if not record["title"]:
        raise ValueError("Include requires a title: " + record["pmid"])
    published = dt.date.fromisoformat(record.get("date", ""))
    if not dt.date.fromisoformat(config["start_date"]) <= published <= today:
        raise ValueError("Publication date outside allowed window: " + record["pmid"])
    if int(record.get("year", 0)) != published.year:
        raise ValueError("Year must match first publication date: " + record["pmid"])
    record["category"] = CATEGORIES.get(record.get("category"))
    if not record["category"]:
        raise ValueError("Include requires spatial/time/spatial, time category")
    if len(str(record.get("evidence", "")).strip()) < 20:
        raise ValueError("Include requires specific evidence of eligibility")
    if not has_sources(record):
        raise ValueError("Include requires a supporting source URL")
    return record


def build_query(config, start, today):
    end = today.isoformat()
    return (f'({config["plant_query"]}) AND ({config["assay_query"]}) AND SRC:MED '
            f'AND FIRST_PDATE:[{config["start_date"]} TO {end}] '
            f'AND (FIRST_IDATE:[{start} TO {end}] OR UPDATE_DATE:[{start} TO {end}] '
            f'OR FIRST_PDATE:[{start} TO {end}])')


def request_bytes(url, config):
    context = ssl.create_default_context()
    try:
        import certifi  # Optional, useful on Python installations without OS roots.
        context = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    for attempt in range(config["retries"] + 1):
        try:
            with urlopen(Request(url, headers={"User-Agent": "PlantLiteratureReview/1.0"}),
                         timeout=config["timeout_seconds"], context=context) as response:
                return response.read()
        except (URLError, TimeoutError, OSError) as error:
            if isinstance(error, HTTPError) and error.code not in {408, 429, 500, 502, 503, 504}:
                raise
            if attempt == config["retries"]:
                raise
            time.sleep(min(2 ** attempt, 8))


def fetch_pages(config, query, get=None):
    get = get or (lambda url: json.loads(request_bytes(url, config)))
    cursor, visited, records = "*", set(), []
    while True:
        if cursor in visited:
            raise ValueError("Europe PMC repeated a pagination cursor")
        visited.add(cursor)
        url = config["endpoint"].rstrip("/") + "/search?" + urlencode({
            "query": query, "format": "json", "resultType": "core",
            "pageSize": config["page_size"], "cursorMark": cursor})
        page = get(url)
        if "resultList" not in page or "hitCount" not in page:
            raise ValueError("Incomplete Europe PMC response; checkpoint unchanged")
        batch = page["resultList"].get("result", [])
        records.extend(batch)
        next_cursor = page.get("nextCursorMark")
        if len(records) >= int(page["hitCount"]):
            break
        if not batch:
            raise ValueError("Empty page before all Europe PMC hits were retrieved; checkpoint unchanged")
        if not next_cursor or next_cursor == cursor:
            raise ValueError("Incomplete Europe PMC pagination; checkpoint unchanged")
        cursor = next_cursor
    return records


def candidate(raw):
    published = raw.get("firstPublicationDate", "")
    return {"pmid": str(raw.get("pmid") or raw.get("id", "")),
            "doi": normalize_doi(raw.get("doi")), "title": clean_title(raw.get("title", "")),
            "date": published, "year": int(published[:4]) if published[:4].isdigit() else None,
            "abstract": raw.get("abstractText", ""), "pmcid": raw.get("pmcid"),
            "publication_types": raw.get("pubTypeList", {}).get("pubType", []),
            "status": "pending", "sources": ["https://pubmed.ncbi.nlm.nih.gov/" + str(raw.get("pmid") or raw.get("id", "")) + "/"]}


def fetch_update(state, config, today, get=None):
    """Pure state update: a failed page can never commit seen keys/checkpoints."""
    prior = state.get("last_fetch", {}).get("through_date")
    start = max(dt.date.fromisoformat(config["start_date"]),
                dt.date.fromisoformat(prior) - dt.timedelta(days=config["overlap_days"]) if prior else today - dt.timedelta(days=config["overlap_days"]))
    query = build_query(config, start.isoformat(), today)
    fetched = deduplicate([candidate(raw) for raw in fetch_pages(config, query, get)])
    deduplicate(state["accepted"] + state["pending"] + fetched)
    updated = copy.deepcopy(state)
    seen = set(updated.get("seen", []))
    added = []
    for record in fetched:
        keys = record_keys(record)
        if not keys & seen:
            added.append(record)
        seen.update(keys)
    updated["pending"].extend(added)
    updated["seen"] = sorted(seen)
    updated["last_fetch"] = {"through_date": today.isoformat(), "query": query,
                             "fetched": len(fetched), "new_pending": len(added),
                             "completed_at": dt.datetime.now(dt.timezone.utc).isoformat()}
    return updated


def apply_decisions(state, decisions, config, today):
    updated = copy.deepcopy(state)
    accepted = {row["pmid"]: row for row in updated["accepted"]}
    pending = {row["pmid"]: row for row in updated["pending"]}
    touched = set()
    for decision in decisions:
        pmid = str(decision.get("pmid", "")).strip()
        if not re.fullmatch(r"[1-9][0-9]*", pmid):
            raise ValueError("Every review decision requires a numeric PMID")
        if pmid in touched:
            raise ValueError("Duplicate review decision: " + pmid)
        touched.add(pmid)
        status = decision.get("status")
        if status not in {"include", "exclude", "pending"}:
            raise ValueError("Decision must explicitly include, exclude or remain pending")
        if pmid in accepted and decision.get("correction") is not True:
            raise ValueError("Existing inclusion requires explicit correction:true: " + pmid)
        merged = {**pending.get(pmid, accepted.get(pmid, {})), **decision, "pmid": pmid}
        if status != "pending" and (len(str(merged.get("evidence", "")).strip()) < 20 or not has_sources(merged)):
            raise ValueError("Include/exclude requires a specific reason and supporting source URL")
        if status == "include":
            accepted[pmid] = validate_include(merged, config, today)
        elif pmid in accepted:
            if status != "exclude":
                raise ValueError("An included record cannot become pending")
            del accepted[pmid]
        if status == "pending":
            pending[pmid] = merged
        else:
            if len(str(decision.get("evidence", "")).strip()) < 20:
                raise ValueError("A review decision requires a specific evidence/reason")
            pending.pop(pmid, None)
            updated["review_log"].append(merged)
    clean = deduplicate(list(accepted.values()))
    if len(clean) != len(accepted):
        raise ValueError("Approved PMID/DOI duplicates require explicit resolution")
    updated["accepted"] = clean
    updated["pending"] = list(pending.values())
    updated["seen"] = sorted(set(updated["seen"]).union(*(record_keys(row) for row in clean + list(pending.values()) + updated["review_log"])))
    return updated


def export_csv(state, directory, today):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(HEADERS)
    for row in sorted(state["accepted"], key=lambda r: (r["date"], int(r["pmid"]))):
        writer.writerow([row["category"], row["year"], row["title"], row["pmid"]])
    content = stream.getvalue().encode("utf-8-sig")
    latest = directory / "latest.csv"
    if latest.exists() and latest.read_bytes() == content:
        return False
    digest = hashlib.sha256(content).hexdigest()[:10]
    atomic_write(directory / "snapshots" / f"plant_papers_{today}_{digest}.csv", content)
    atomic_write(latest, content)
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=HOME / "config.json")
    parser.add_argument("--data-dir", type=Path, default=HOME / "data")
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("init", help="Import the reviewed baseline once")
    initialize.add_argument("--baseline", type=Path, required=True)
    retrieve = commands.add_parser("fetch", help="Fetch candidates; never approve them")
    retrieve.add_argument("--today", help="ISO date, cannot exceed today's local date")
    publish = commands.add_parser("publish", help="Apply explicit review decisions and export")
    publish.add_argument("--decisions", type=Path, required=True)
    commands.add_parser("status", help="Show successful fetch and independent review counts")
    text = commands.add_parser("fulltext", help="Save available Europe PMC full-text XML")
    text.add_argument("pmcid")
    args = parser.parse_args(argv)
    config, directory = read_json(args.config), args.data_dir.resolve()
    today = local_today(config)
    if getattr(args, "today", None):
        requested = dt.date.fromisoformat(args.today)
        if requested > today:
            raise ValueError("--today cannot exceed the configured timezone's current date")
        today = requested
    state_path = directory / "state.json"
    if args.command == "fulltext":
        if not re.fullmatch(r"PMC[0-9]+", args.pmcid):
            raise ValueError("Expected a PMCID such as PMC12345678")
        body = request_bytes(config["endpoint"].rstrip("/") + "/" + args.pmcid + "/fullTextXML", config)
        atomic_write(directory / "fulltext" / (args.pmcid + ".xml"), body)
        return
    if args.command == "status":
        state = read_json(state_path)
        print(json.dumps({"accepted": len(state["accepted"]), "pending": len(state["pending"]),
                          "baseline_count": state["baseline_count"], "last_fetch": state["last_fetch"]}, indent=2))
        return
    with state_lock(directory):
        return run_mutation(args, config, directory, today, state_path)


def run_mutation(args, config, directory, today, state_path):
    """Run an initialized CLI operation under the shared state lock."""
    if args.command == "init":
        if state_path.exists():
            raise ValueError("Already initialized; baseline import will not overwrite state")
        baseline = [validate_include(row, config, today) for row in read_json(args.baseline)]
        rows = deduplicate(baseline)
        if len(rows) != len(baseline):
            raise ValueError("Baseline contains duplicate identities")
        state = {"schema_version": 1, "baseline_count": len(rows), "accepted": rows,
                 "pending": [], "review_log": [], "seen": sorted(set().union(*(record_keys(row) for row in rows))),
                 "last_fetch": {}}
    else:
        state = read_json(state_path)
        if args.command == "fetch":
            state = fetch_update(state, config, today)
        elif args.command == "publish":
            state = apply_decisions(state, read_json(args.decisions)["decisions"], config, today)
    save_json(state_path, state)
    # Exports are reconstructible from authoritative state if interrupted here.
    changed = export_csv(state, directory, today)
    save_json(directory / "pending_review.json", {"candidates": state["pending"]})
    print(json.dumps({"accepted": len(state["accepted"]), "pending": len(state["pending"]),
                      "csv_changed": changed, "last_fetch": state["last_fetch"]}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, URLError) as error:
        print("Error: " + str(error), file=sys.stderr)
        sys.exit(1)
