"""Wire-parser regressions; no sockets, secrets, or network requests."""
import hashlib
import http.client
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout

spec = importlib.util.spec_from_file_location("accept_lens", Path(__file__).with_name("accept_lens.py"))
lens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lens)


class WireSocket:
    def __init__(self, wire):
        self.wire = wire

    def makefile(self, *args):
        return io.BytesIO(self.wire)


class WireConnection:
    sock = None

    def __init__(self, wire):
        self.response = http.client.HTTPResponse(WireSocket(wire))
        self.closed = False

    def request(self, method, target, headers):
        assert method == "GET"
        assert headers["User-Agent"] == lens.USER_AGENT

    def getresponse(self):
        self.response.begin()
        return self.response

    def close(self):
        self.closed = True
        self.response.close()


def observe(wire, cap=100):
    connection = WireConnection(wire)
    result = lens.observe("https://api.imd.fun/launches", "application/json", cap, 1,
                          lambda *args, **kwargs: connection)
    assert connection.closed
    return result


def response(body, headers=b"Content-Length: 50", status=b"200 OK"):
    return b"HTTP/1.1 " + status + b"\r\nContent-Type: application/json\r\n" + headers + b"\r\n\r\n" + body


class TruncationTests(unittest.TestCase):
    def test_valid_json_with_short_content_length_is_incomplete(self):
        report = observe(response(b"{}"))
        self.assertFalse(report["ok"])
        self.assertFalse(report["body_complete"])
        self.assertEqual(report["body_bytes"], 2)
        self.assertEqual(report["expected_body_bytes"], 50)
        self.assertIn("Content-Length", report["error"]["message"])
        self.assertNotIn("body_sha256", report)
        self.assertNotIn("valid_json", report)
        self.assertEqual(lens.compare([report, report])["verdict"], "incomplete")

    def test_empty_short_response_is_incomplete(self):
        report = observe(response(b""))
        self.assertFalse(report["ok"])
        self.assertEqual(report["body_bytes"], 0)

    def test_parent_and_cli_keep_short_body_as_failure(self):
        def worker(command, **kwargs):
            sample = observe(response(b"{}"))
            sample["accept"] = command[-3]
            return subprocess.CompletedProcess(command, 0, json.dumps(sample), "")

        result = lens.run("https://api.imd.fun/launches", 2, 100, worker)
        self.assertEqual(result["comparison"]["verdict"], "incomplete")
        self.assertEqual(len(result["samples"]), 2)
        self.assertTrue(all(s["ok"] is False for s in result["samples"]))
        output = io.StringIO()
        with patch.object(lens, "run", return_value=result), redirect_stdout(output):
            code = lens.main(["https://api.imd.fun/launches"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())["comparison"]["verdict"], "incomplete")

    def test_exact_length_response_is_complete(self):
        report = observe(response(b"{}", b"Content-Length: 2"))
        self.assertTrue(report["ok"])
        self.assertTrue(report["body_complete"])
        self.assertTrue(report["valid_json"])
        self.assertEqual(report["body_sha256"], hashlib.sha256(b"{}").hexdigest())

    def test_zero_length_is_complete_without_json(self):
        report = observe(response(b"", b"Content-Length: 0"))
        self.assertTrue(report["ok"])
        self.assertTrue(report["body_complete"])
        self.assertFalse(report["valid_json"])

    def test_304_length_is_representation_metadata(self):
        report = observe(response(b"", b"Content-Length: 50", b"304 Not Modified"))
        self.assertTrue(report["ok"])
        self.assertEqual(report["expected_body_bytes"], 0)
        self.assertEqual(report["body_bytes"], 0)

    def test_204_has_no_message_body(self):
        report = observe(response(b"", b"", b"204 No Content"))
        self.assertTrue(report["ok"])
        self.assertEqual(report["expected_body_bytes"], 0)

    def test_close_delimited_response_keeps_library_eof_semantics(self):
        report = observe(response(b"{}", b"Connection: close"))
        self.assertTrue(report["ok"])
        self.assertTrue(report["body_complete"])
        self.assertNotIn("expected_body_bytes", report)

    def test_complete_chunked_transfer(self):
        report = observe(response(b"2\r\n{}\r\n0\r\n\r\n", b"Transfer-Encoding: chunked"))
        self.assertTrue(report["ok"])
        self.assertTrue(report["body_complete"])
        self.assertEqual(report["body_bytes"], 2)

    def test_chunked_transfer_without_terminator_is_incomplete(self):
        report = observe(response(b"2\r\n{}\r\n", b"Transfer-Encoding: chunked"))
        self.assertFalse(report["ok"])
        self.assertFalse(report["body_complete"])
        self.assertNotIn("body_sha256", report)

    def test_chunk_body_cut_short_is_incomplete(self):
        report = observe(response(b"8\r\n{}", b"Transfer-Encoding: chunked"))
        self.assertFalse(report["ok"])
        self.assertFalse(report["body_complete"])
        self.assertNotIn("body_sha256", report)

    def test_byte_limit_still_takes_priority(self):
        report = observe(response(b"{}", b"Content-Length: 2"), cap=1)
        self.assertFalse(report["ok"])
        self.assertFalse(report["body_complete"])
        self.assertIn("byte limit", report["error"]["message"])


if __name__ == "__main__":
    unittest.main()
