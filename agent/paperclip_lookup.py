#!/usr/bin/env python3
"""Optional authenticated Paperclip lookup; not a literature discovery source.

Reads PAPERCLIP_API_KEY from the environment and never persists credentials.
Official API reference: https://paperclip.gxl.ai/docs (HTTP API section).
"""

import argparse
import datetime as dt
import email.utils
import json
import os
from pathlib import Path
import re
import ssl
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request


API_BASE = "https://paperclip.gxl.ai/api/v1"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "data" / "paperclip"


class PaperclipError(Exception):
    """An error safe to show without exposing request headers or bodies."""


def validate_pmid(value):
    if not re.fullmatch(r"[0-9]{8}", value):
        raise argparse.ArgumentTypeError("PMID must contain exactly 8 digits")
    return value


def validate_doi(value):
    value = value.strip()
    if not re.fullmatch(r"10\.[0-9]{4,9}/[^\s]+", value, re.IGNORECASE):
        raise argparse.ArgumentTypeError("DOI must be an identifier such as 10.1038/example")
    return value


def tls_context():
    # certifi is optional. No package installation is required.
    try:
        import certifi
    except ImportError:
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


def retry_delay(headers, attempt):
    value = headers.get("Retry-After", "") if headers else ""
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        try:
            retry_at = email.utils.parsedate_to_datetime(value)
            if retry_at.tzinfo is None:
                retry_at = retry_at.replace(tzinfo=dt.timezone.utc)
            seconds = (retry_at - dt.datetime.now(dt.timezone.utc)).total_seconds()
        except (TypeError, ValueError, OverflowError):
            seconds = 2 ** attempt
    return max(0, min(seconds, 30))


def request_json(path, api_key, payload=None, timeout=30, retries=3):
    """Request JSON, retrying rate limits, server errors, and transient transport errors."""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"X-API-Key": api_key, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    context = tls_context()
    for attempt in range(retries + 1):
        request = urllib.request.Request(
            API_BASE + path, data=data, headers=headers,
            method="POST" if payload is not None else "GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                raw = response.read()
            try:
                return json.loads(raw)
            except (ValueError, UnicodeDecodeError):
                raise PaperclipError("Paperclip returned a response that was not valid JSON") from None
        except urllib.error.HTTPError as exc:
            status = exc.code
            delay = retry_delay(exc.headers, attempt)
            exc.close()
            if (status == 429 or 500 <= status <= 599) and attempt < retries:
                time.sleep(delay)
                continue
            raise PaperclipError(f"Paperclip request failed (HTTP {status})") from None
        except (urllib.error.URLError, TimeoutError, OSError):
            if attempt < retries:
                time.sleep(min(2 ** attempt, 30))
                continue
            raise PaperclipError("Paperclip could not be reached after retries") from None


def lookup_pmid(response):
    """Read only the returned paper's PMID; do not search references for identifiers."""
    if isinstance(response, dict):
        value = str(response.get("pmid", ""))
        if re.fullmatch(r"[0-9]{8}", value):
            return value
    return None


def save_json(destination, value):
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix=".paperclip-", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    identity = parser.add_mutually_exclusive_group(required=True)
    identity.add_argument("--pmid", type=validate_pmid)
    identity.add_argument("--doi", type=validate_doi)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout", type=int, default=30, help="Seconds per request (default: 30)")
    args = parser.parse_args(argv)
    if not 1 <= args.timeout <= 120:
        parser.error("--timeout must be between 1 and 120 seconds")

    api_key = os.environ.get("PAPERCLIP_API_KEY", "").strip()
    if not api_key:
        print("Paperclip enrichment skipped: PAPERCLIP_API_KEY is not set.", file=sys.stderr)
        return 3

    kind = "pmid" if args.pmid else "doi"
    identifier = args.pmid or args.doi
    try:
        result = request_json("/lookup", api_key, {kind: identifier}, timeout=args.timeout)
        pmid = args.pmid or lookup_pmid(result)
        output = {
            "identifier": {kind: identifier},
            "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "source": "Paperclip optional enrichment",
            "lookup": result,
        }
        if pmid:
            output["document"] = request_json(
                "/documents/pmid:" + validate_pmid(pmid), api_key, timeout=args.timeout,
            )
        else:
            output["document_status"] = "No 8-digit PMID in the lookup object; document request skipped"

        # Encode DOI slashes and other path characters to keep output inside one directory.
        filename = kind + "-" + urllib.parse.quote(identifier, safe="") + ".json"
        destination = args.output_dir / filename
        save_json(destination, output)
    except PaperclipError as exc:
        # Do not print remote response bodies, headers, credentials, or exception details.
        print(f"{exc}; no output was published.", file=sys.stderr)
        return 1
    except OSError:
        print("Paperclip enrichment could not write its output file.", file=sys.stderr)
        return 1
    print(f"Saved optional Paperclip enrichment: {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
