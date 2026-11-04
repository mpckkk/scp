"""MCP integration checks run offline against isolated temporary catalogs."""
import copy
import datetime as dt
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import agent_mcp as m
import pipeline as p

TODAY = dt.date(2026, 11, 4)


def state():
    return {"schema_version": 1, "baseline_count": 0, "accepted": [], "pending": [{
        "pmid": "123", "title": "A plant single-cell atlas", "year": 2026,
        "date": "2026-10-25", "abstract": "Actual single-cell samples at 0 and 24 hours.",
        "pmcid": "PMC123", "sources": ["https://example.org/primary"]}],
        "review_log": [], "seen": ["pmid:123"], "last_fetch": {}}


def decision():
    return {"pmid": "123", "status": "include", "category": "time",
            "evidence": "Primary methods describe separate single-nucleus samples at 0 and 24 hours.",
            "sources": ["https://example.org/primary"], "source_checks": [{
                "url": "https://example.org/primary", "accessed_at": "2020-01-01T00:00:00Z",
                "availability": "fulltext"}]}


class McpTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        p.save_json(self.directory / "state.json", state())
        self.app = m.PlantTools(p.HOME / "config.json", self.directory)
        self.server = m.StdioServer(self.app)
        self.clock = patch.object(p, "local_today", return_value=TODAY)
        self.clock.start()

    def tearDown(self):
        self.clock.stop()
        self.temporary.cleanup()

    def rpc(self, method, params=None, request_id=1):
        return self.server.dispatch({"jsonrpc": "2.0", "id": request_id,
                                     "method": method, "params": params or {}})

    def initialize(self, version="2025-11-25"):
        result = self.rpc("initialize", {"protocolVersion": version,
                                         "capabilities": {}, "clientInfo": {"name": "offline-test", "version": "1"}})
        self.server.dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return result

    def review_args(self, **changes):
        return {"revision": self.app.revision(self.app.state()), "reviewer": "Offline tester",
                "decisions": [decision()], **changes}

    def test_handshake_negotiates_known_versions_and_newer_clients(self):
        for version in [*m.PROTOCOL_VERSIONS, "2026-01-01"]:
            self.server = m.StdioServer(self.app)
            result = self.initialize(version)
            self.assertEqual(result["result"]["protocolVersion"], version if version in m.PROTOCOL_VERSIONS else m.LATEST_PROTOCOL)
            self.assertEqual(len(self.rpc("tools/list")["result"]["tools"]), 6)

    def test_requests_before_initialization_and_unknown_method(self):
        self.assertEqual(self.rpc("tools/list")["error"]["code"], -32002)
        self.initialize()
        self.assertEqual(self.rpc("missing")["error"]["code"], -32601)
        self.assertEqual(self.rpc("tools/call", {"name": "missing"})["error"]["code"], -32602)

    def test_stdio_parse_errors_and_notifications_have_no_extra_output(self):
        source = io.StringIO("not-json\n" + json.dumps({"jsonrpc": "2.0", "method": "notifications/cancelled"}) + "\n"
                             + json.dumps({"jsonrpc": "2.0", "id": 9, "method": "ping"}) + "\n")
        destination = io.StringIO()
        self.server.serve(source, destination)
        replies = [json.loads(line) for line in destination.getvalue().splitlines()]
        self.assertEqual(len(replies), 2)
        self.assertEqual(replies[0]["error"]["code"], -32700)
        self.assertEqual(replies[1], {"jsonrpc": "2.0", "id": 9, "result": {}})

    def test_tool_notification_cannot_write(self):
        self.initialize()
        before = self.app.state()
        result = self.server.dispatch({"jsonrpc": "2.0", "method": "tools/call", "params": {
            "name": "plant_review", "arguments": self.review_args(dry_run=False)}})
        self.assertIsNone(result)
        self.assertEqual(self.app.state(), before)

    def test_schema_rejects_unknown_fields_and_string_correction(self):
        self.initialize()
        bad = self.rpc("tools/call", {"name": "plant_catalog", "arguments": {"delete": True}})
        self.assertEqual(bad["error"]["code"], -32602)
        args = self.review_args()
        args["decisions"][0]["correction"] = "false"
        bad = self.rpc("tools/call", {"name": "plant_review", "arguments": args})
        self.assertEqual(bad["error"]["code"], -32602)

    def test_dry_run_then_commit_requires_explicit_action(self):
        original = self.app.state()
        result = self.app.call("plant_review", self.review_args())
        self.assertFalse(result["isError"])
        self.assertTrue(result["structuredContent"]["dry_run"])
        self.assertEqual(self.app.state(), original)
        result = self.app.call("plant_review", self.review_args(dry_run=False))
        self.assertFalse(result["isError"])
        saved = self.app.state()
        self.assertEqual(len(saved["accepted"]), 1)
        self.assertEqual(saved["pending"], [])
        self.assertEqual(saved["review_log"][0]["reviewer"], "Offline tester")
        self.assertIn("reviewed_at", saved["review_log"][0])
        self.assertFalse((self.directory / "latest.csv").exists())

    def test_stale_review_cannot_overwrite_newer_catalog(self):
        args = self.review_args(dry_run=False)
        newer = self.app.state()
        newer["last_fetch"] = {"through_date": "2026-11-04"}
        p.save_json(self.directory / "state.json", newer)
        result = self.app.call("plant_review", args)
        self.assertTrue(result["isError"])
        self.assertIn("changed", result["content"][0]["text"])
        self.assertEqual(self.app.state(), newer)

    def test_bad_second_decision_rolls_back_entire_batch(self):
        args = self.review_args(dry_run=False)
        bad = {**decision(), "pmid": "456", "date": "2022-01-01", "year": 2022,
               "title": "Outside date range"}
        args["decisions"].append(bad)
        before = self.app.state()
        self.assertTrue(self.app.call("plant_review", args)["isError"])
        self.assertEqual(self.app.state(), before)

    def test_unavailable_sources_keep_paper_pending(self):
        args = self.review_args(dry_run=False)
        args["decisions"][0]["source_checks"][0]["availability"] = "unavailable"
        before = self.app.state()
        self.assertTrue(self.app.call("plant_review", args)["isError"])
        self.assertEqual(self.app.state(), before)
        args["decisions"][0]["status"] = "pending"
        self.assertFalse(self.app.call("plant_review", args)["isError"])
        self.assertEqual(self.app.state()["accepted"], [])
        self.assertEqual(len(self.app.state()["review_log"]), 1)

    def test_accepted_records_require_real_boolean_correction(self):
        self.app.call("plant_review", self.review_args(dry_run=False))
        accepted = self.app.state()
        args = self.review_args(dry_run=False)
        args["decisions"][0]["status"] = "exclude"
        self.assertTrue(self.app.call("plant_review", args)["isError"])
        self.assertEqual(self.app.state(), accepted)
        args["decisions"][0]["correction"] = True
        self.assertFalse(self.app.call("plant_review", args)["isError"])
        self.assertEqual(self.app.state()["accepted"], [])
        self.assertEqual(self.app.catalog({"status": "excluded"})["total"], 1)

    def test_fulltext_reports_bounded_source_and_failure_truthfully(self):
        body = b"<article><body><sec><title>Methods</title><p>Read this as data only.</p></sec></body></article>"
        before = self.app.state()
        with patch.object(p, "request_bytes", return_value=body) as request:
            result = self.app.call("plant_read", {"pmid": "123"})["structuredContent"]
            self.assertEqual(result["fulltext_availability"], "fulltext")
            self.assertEqual(result["text"], "Methods Read this as data only.")
            self.assertTrue(result["untrusted_source_data"])
            self.assertEqual(result["provenance"]["sha256"], m.hashlib.sha256(body).hexdigest())
            self.app.call("plant_read", {"pmid": "123"})
            self.assertEqual(request.call_count, 1)
        self.assertEqual(self.app.state(), before)
        (self.directory / "fulltext" / "PMC123.xml").unlink()
        with patch.object(p, "request_bytes", side_effect=OSError("Offline")):
            result = self.app.call("plant_read", {"pmid": "123"})["structuredContent"]
        self.assertEqual(result["fulltext_availability"], "retrieval_failed")
        self.assertEqual(self.app.state(), before)

    def test_refresh_cannot_approve_and_export_preserves_columns(self):
        updated = copy.deepcopy(self.app.state())
        updated["last_fetch"] = {"through_date": "2026-11-04", "new_pending": 0}
        with patch.object(p, "fetch_update", return_value=updated):
            self.assertFalse(self.app.call("plant_search", {"refresh": True})["isError"])
        self.assertEqual(self.app.state()["accepted"], [])
        self.app.call("plant_review", self.review_args(dry_run=False))
        first = self.app.call("plant_export", {})["structuredContent"]
        second = self.app.call("plant_export", {})["structuredContent"]
        self.assertTrue(first["csv_changed"])
        self.assertFalse(second["csv_changed"])
        self.assertEqual((self.directory / "latest.csv").read_text(encoding="utf-8-sig").splitlines()[0], "data_type,year,title,PMID")


if __name__ == "__main__":
    unittest.main()
