"""Offline regression checks: python3 -m unittest discover -s . -v"""
import copy
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from urllib.parse import parse_qs, urlparse
import pipeline as p

TODAY = dt.date(2026, 11, 4)
CONFIG = json.loads((Path(__file__).parent / "config.json").read_text())


def state():
    return {"accepted": [], "pending": [], "review_log": [], "seen": [],
            "last_fetch": {}, "baseline_count": 0}


def raw(pmid="123", doi="10.1/test"):
    return {"id": pmid, "title": "A plant single-cell atlas", "doi": doi,
            "firstPublicationDate": "2026-10-25"}


def reviewed(pmid="123"):
    return {"pmid": pmid, "title": "A plant single-cell atlas", "year": 2026,
            "date": "2026-10-25", "category": "time", "status": "include",
            "evidence": "Single-nucleus RNA samples at 0, 12 and 24 hours.",
            "sources": ["https://pubmed.ncbi.nlm.nih.gov/" + pmid + "/"]}


class PipelineTests(unittest.TestCase):
    def test_pagination(self):
        cursors = []
        def get(url):
            cursor = parse_qs(urlparse(url).query)["cursorMark"][0]
            cursors.append(cursor)
            return {"hitCount": 2, "nextCursorMark": "next",
                    "resultList": {"result": [raw("1" if cursor == "*" else "2")]}}
        self.assertEqual(len(p.fetch_pages(CONFIG, "query", get)), 2)
        self.assertEqual(cursors, ["*", "next"])

    def test_duplicate_doi_is_normalized(self):
        a, b = p.candidate(raw("1", "https://doi.org/10.1/TEST")), p.candidate(raw("2", "doi:10.1/test"))
        self.assertEqual(len(p.deduplicate([a, b])), 1)
        b["title"] = "Conflicting article"
        with self.assertRaises(ValueError):
            p.deduplicate([a, b])

    def test_empty_result_is_success_not_approval(self):
        updated = p.fetch_update(state(), CONFIG, TODAY, lambda _: {"hitCount": 0, "resultList": {"result": []}})
        self.assertEqual(updated["last_fetch"]["through_date"], "2026-11-04")
        self.assertEqual(updated["accepted"], [])

    def test_empty_page_with_unretrieved_hits_is_failure(self):
        initial = state()
        with self.assertRaises(ValueError):
            p.fetch_update(initial, CONFIG, TODAY,
                           lambda _: {"hitCount": 4, "resultList": {"result": []}})
        self.assertEqual(initial, state())

    def test_encoded_and_raw_title_html_matches_plain_baseline(self):
        plain = p.candidate(raw())
        for title in ["A plant <i>single-cell</i> atlas", "A plant &lt;i&gt;single-cell&lt;/i&gt; atlas"]:
            record = p.candidate({**raw(), "title": title})
            self.assertEqual(record["title"], plain["title"])
            self.assertEqual(len(p.deduplicate([plain, record])), 1)

    def test_all_decisions_require_pmid_and_exclusions_require_source(self):
        for status in ["include", "exclude", "pending"]:
            with self.assertRaises(ValueError):
                p.apply_decisions(state(), [{"status": status}], CONFIG, TODAY)
        excluded = {"pmid": "321", "status": "exclude",
                    "evidence": "Primary methods show only one sampled time point."}
        with self.assertRaises(ValueError):
            p.apply_decisions(state(), [excluded], CONFIG, TODAY)
        excluded["sources"] = ["https://pubmed.ncbi.nlm.nih.gov/321/"]
        result = p.apply_decisions(state(), [excluded], CONFIG, TODAY)
        self.assertIn("pmid:321", result["seen"])

    def test_fetch_never_approves_and_persistently_deduplicates(self):
        getter = lambda _: {"hitCount": 1, "resultList": {"result": [raw()]}}
        initial = state()
        updated = p.fetch_update(initial, CONFIG, TODAY, getter)
        self.assertEqual(initial, state())
        self.assertEqual(updated["pending"][0]["status"], "pending")
        self.assertEqual(updated["accepted"], [])
        again = p.fetch_update(updated, CONFIG, TODAY, getter)
        self.assertEqual(len(again["pending"]), 1)

    def test_failed_page_does_not_mutate_state(self):
        initial = state()
        original = copy.deepcopy(initial)
        calls = []
        def get(_):
            calls.append(1)
            if len(calls) == 2:
                raise OSError("network failure")
            return {"hitCount": 2, "nextCursorMark": "next", "resultList": {"result": [raw()]}}
        with self.assertRaises(OSError):
            p.fetch_update(initial, CONFIG, TODAY, get)
        self.assertEqual(initial, original)

    def test_include_requires_evidence_source_and_eligible_date(self):
        for changes in [{"date": "2026-11-05"}, {"date": "2022-01-01", "year": 2022},
                        {"sources": []}, {"evidence": "keyword hit"}, {"year": 2025}]:
            with self.assertRaises((ValueError, TypeError)):
                p.validate_include({**reviewed(), **changes}, CONFIG, TODAY)

    def test_explicit_decision_and_correction(self):
        initial = state()
        initial["pending"] = [p.candidate(raw())]
        approved = p.apply_decisions(initial, [reviewed()], CONFIG, TODAY)
        self.assertEqual(len(approved["accepted"]), 1)
        self.assertEqual(approved["pending"], [])
        excluded = {"pmid": "123", "status": "exclude", "evidence": "Review established only one sampled time point."}
        with self.assertRaises(ValueError):
            p.apply_decisions(approved, [excluded], CONFIG, TODAY)
        fixed = p.apply_decisions(approved, [{**excluded, "correction": True}], CONFIG, TODAY)
        self.assertEqual(fixed["accepted"], [])

    def test_query_overlap_and_broad_assay(self):
        query = p.build_query(CONFIG, "2026-10-07", TODAY)
        self.assertIn("FIRST_IDATE:[2026-10-07 TO 2026-11-04]", query)
        self.assertIn("UPDATE_DATE:[2026-10-07 TO 2026-11-04]", query)
        self.assertIn("FIRST_PDATE:[2023-01-01 TO 2026-11-04]", query)
        self.assertNotIn("AND TITLE_ABS:time", query)

    def test_exports_only_change_when_approved_content_changes(self):
        current = state()
        current["accepted"] = [reviewed()]
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.assertTrue(p.export_csv(current, directory, TODAY))
            self.assertFalse(p.export_csv(current, directory, TODAY + dt.timedelta(days=1)))
            self.assertEqual(len(list((directory / "snapshots").glob("*.csv"))), 1)
            self.assertEqual((directory / "latest.csv").read_text(encoding="utf-8-sig").splitlines()[0], "data_type,year,title,PMID")


if __name__ == "__main__":
    unittest.main()
