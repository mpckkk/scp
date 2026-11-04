"""Offline tests: no authenticated or network requests are performed."""

import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import paperclip_lookup as paperclip


class PaperclipTests(unittest.TestCase):
    def test_missing_key_skips_without_request(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(paperclip, "request_json") as request:
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                code = paperclip.main(["--pmid", "37321217"])
        self.assertEqual(code, 3)
        self.assertIn("PAPERCLIP_API_KEY is not set", stderr.getvalue())
        request.assert_not_called()

    def test_lookup_and_document_persist_without_credentials(self):
        key = "offline-test-secret"
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict(os.environ, {"PAPERCLIP_API_KEY": key}), patch.object(
                paperclip, "request_json", side_effect=[{"pmid": "37321217"}, {"text": "Methods"}]
            ) as request, contextlib.redirect_stdout(io.StringIO()):
                code = paperclip.main(["--pmid", "37321217", "--output-dir", folder])
            saved = Path(folder, "pmid-37321217.json").read_text()
        self.assertEqual(code, 0)
        self.assertNotIn(key, saved)
        self.assertEqual(json.loads(saved)["document"]["text"], "Methods")
        self.assertEqual(request.call_args_list[0].args[0], "/lookup")
        self.assertEqual(request.call_args_list[1].args[0], "/documents/pmid:37321217")

    def test_rate_limit_retries_without_network(self):
        error = urllib.error.HTTPError("https://example.invalid", 429, "rate limit", {"Retry-After": "0"}, io.BytesIO(b""))
        response = contextlib.nullcontext(io.BytesIO(b'{"pmid":"37321217"}'))
        with patch.object(paperclip, "tls_context"), patch.object(
            paperclip.urllib.request, "urlopen", side_effect=[error, response]
        ) as request, patch.object(paperclip.time, "sleep") as sleep:
            result = paperclip.request_json("/lookup", "offline-test-secret", {"pmid": "37321217"})
        self.assertEqual(result["pmid"], "37321217")
        self.assertEqual(request.call_count, 2)
        sleep.assert_called_once_with(0)


if __name__ == "__main__":
    unittest.main()
