"""Unit tests that run without Streamlit or network access."""

import os
import unittest
from datetime import datetime, timezone

from streamlit.testing.v1 import AppTest

from analyzer import MAX_BYTES, analyze, normalize_message, parse_line, to_markdown

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


class TestAnalyzer(unittest.TestCase):
    def test_plain_text_and_jsonl(self):
        text = ('2026-06-27 10:00:01 INFO Connection established 42\n'
                '{"timestamp":"2026-06-27T10:00:02Z","level":"error","message":"DB failed"}\n'
                'bad line\n')
        result = analyze(text)
        self.assertEqual(result["matched_lines"], 2)
        self.assertEqual(result["invalid_lines"], 1)
        self.assertEqual(result["levels"], {"ERROR": 1, "INFO": 1})
        self.assertEqual({item["level"] for item in result["patterns"]}, {"ERROR", "INFO"})

    def test_error_burst(self):
        text = "\n".join(f"2026-06-27 10:00:{i:02d} ERROR failure {i}" for i in range(4))
        result = analyze(text)
        self.assertEqual(len(result["error_bursts"]), 1)
        self.assertEqual(result["error_bursts"][0]["error_count"], 4)

    def test_time_filter_and_normalization(self):
        text = ('2026-06-27 10:00:01 INFO Request ID 100\n'
                '2026-06-28 10:00:01 INFO Request ID 200\n')
        result = analyze(text, end=datetime(2026, 6, 27, 23, 59, tzinfo=timezone.utc))
        self.assertEqual(result["matched_lines"], 1)
        self.assertEqual(result["outside_time_range"], 1)
        self.assertEqual(normalize_message("Request ID 100"), "Request ID <num>")

    def test_secret_redaction_and_report(self):
        result = analyze("2026-06-27 10:00:01 INFO token=abc123 user=john@example.com\n")
        report = to_markdown(result)
        self.assertNotIn("abc123", report)
        self.assertNotIn("john@example.com", report)
        self.assertIn("<redacted>", report)

    def test_common_text_formats(self):
        text = (
            "2026-11-22T09:00:00.100Z [INFO] [main] Application started\n"
            "2026-11-22 09:00:01,321 WARN com.example.App - slow response\n"
            "2026-11-22 09:00:02 connection pool healthy\n"
        )
        result = analyze(text)
        self.assertEqual(result["matched_lines"], 3)
        self.assertEqual(result["levels"], {"INFO": 1, "UNKNOWN": 1, "WARN": 1})
        self.assertEqual(result["detected_formats"], {"text": 3})
        self.assertEqual(result["parse_success_percent"], 100)

    def test_kubernetes_cri_wrapped_log(self):
        text = (
            "2026-11-22T09:00:00.123456789Z stdout F 2026-11-22T09:00:00.1Z ERROR timed out\n"
            "2026-11-22T09:00:01.123456789Z stderr F startup without level\n"
        )
        result = analyze(text)
        self.assertEqual(result["levels"], {"ERROR": 1, "UNKNOWN": 1})
        self.assertEqual(result["detected_formats"], {"kubernetes-cri": 2})

    def test_docker_json_envelope_and_epoch(self):
        text = (
            '{"time":"2026-11-22T09:00:00Z","stream":"stdout","log":"INFO Worker ready"}\n'
            '{"ts":1795338000000,"severity":"ERROR","msg":"DB timeout"}\n'
        )
        result = analyze(text)
        self.assertEqual(result["levels"], {"ERROR": 1, "INFO": 1})
        self.assertEqual(result["matched_lines"], 2)

    def test_safe_failure_diagnostics(self):
        result = analyze('not a log\n{"timestamp":"bad","level":"INFO","message":"secret=abc"}\n'
                         '{"timestamp":"2026-11-22T09:00:00Z","msg":"safe"}\n')
        self.assertEqual(result["invalid_lines"], 2)
        self.assertEqual(result["parse_failures"], {
            "invalid_timestamp": 1, "unsupported_prefix": 1,
        })
        self.assertEqual(result["levels"], {"UNKNOWN": 1})
        self.assertNotIn("secret=abc", str(result))

    def test_zero_parsed_data_has_valid_empty_statistics(self):
        result = analyze("unrecognized\nalso unrecognized\n")
        self.assertEqual(result["matched_lines"], 0)
        self.assertEqual(result["levels"], {})
        self.assertEqual(result["patterns"], [])
        self.assertEqual(result["detected_formats"], {})
        self.assertEqual(result["parse_failures"], {"unsupported_prefix": 2})

    def test_empty_time_selection_has_no_crash_data(self):
        result = analyze("2026-11-22 09:00:00 INFO started",
                         start=datetime(2026, 11, 23, tzinfo=timezone.utc))
        self.assertEqual(result["matched_lines"], 0)
        self.assertEqual(result["outside_time_range"], 1)
        self.assertEqual(result["levels"], {})

    def test_limits_and_empty_input(self):
        self.assertEqual(analyze("")["matched_lines"], 0)
        with self.assertRaises(ValueError):
            analyze("x" * (MAX_BYTES + 1))
        self.assertIsNone(parse_line("nonsense"))
    def test_logfmt_multiline_fixture(self):
        with open(os.path.join(FIXTURES, "logfmt_multiline.log"), encoding="utf-8") as handle:
            result = analyze(handle.read())
        self.assertEqual(result["detected_format"], "logfmt")
        self.assertEqual(result["matched_lines"], 3)
        self.assertEqual(result["continuation_lines"], 3)
        self.assertEqual(result["invalid_lines"], 0)
        self.assertEqual(result["levels"], {"ERROR": 1, "INFO": 1, "WARN": 1})
        self.assertEqual(result["error_bursts"], [])
        self.assertEqual(result["parse_success_percent"], 100)

    def test_manual_parser_selection(self):
        line = 'time="2026-06-27T10:00:00Z" level=info msg="started"\n'
        self.assertEqual(analyze(line, parser="logfmt")["matched_lines"], 1)
        self.assertEqual(analyze(line, parser="jsonl")["matched_lines"], 0)
        with self.assertRaises(ValueError):
            analyze(line, parser="no-such-parser")

    def test_custom_rules_fixture(self):
        with open(os.path.join(FIXTURES, "app_rules.json"), encoding="utf-8") as handle:
            rules = handle.read()
        text = "[2026-06-27 10:00:00] SEVERE queue stalled\n[2026-06-27 10:00:01] INFO recovered\n"
        result = analyze(text, rules_text=rules)
        self.assertEqual(result["detected_formats"], {"acme-app": 2})
        self.assertEqual(result["levels"], {"ERROR": 1, "INFO": 1})
        with self.assertRaises(ValueError):
            analyze(text, rules_text='{"rules": [{"name": "bad", "pattern": "^(?P<level>x)$"}]}')

    def test_partial_parse_reports_invalid_timestamp(self):
        text = ("2026-06-27 10:00:00 INFO good line\n"
                "2026-13-45 10:00:00 INFO impossible date\n")
        result = analyze(text)
        self.assertEqual(result["matched_lines"], 1)
        self.assertEqual(result["parse_failures"], {"invalid_timestamp": 1})
        self.assertEqual(result["malformed_lines"], 1)
        self.assertEqual(result["unsupported_lines"], 0)
        self.assertEqual(result["parse_success_percent"], 50.0)


class TestAppEmptyStates(unittest.TestCase):
    APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")

    def _run(self, text=None):
        at = AppTest.from_file(self.APP, default_timeout=30).run()
        if text is not None:
            at.text_area[0].input(text).run()
        return at

    def test_empty_input_shows_prompt_without_exception(self):
        at = self._run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.get("vega_lite_chart")), 0)

    def test_unsupported_format_shows_message_and_no_charts(self):
        at = self._run("this is not a log format\nneither is this\n")
        self.assertFalse(at.exception)
        self.assertIn("No matching log format detected.", [w.value for w in at.warning])
        self.assertEqual(len(at.get("vega_lite_chart")), 0)
        self.assertEqual(len(at.get("dataframe")), 0)

    def test_valid_logfmt_renders_charts(self):
        at = self._run('time="2026-06-27T10:00:00Z" level=info msg="started"\n'
                       'time="2026-06-27T10:00:01Z" level=error msg="failed"\n')
        self.assertFalse(at.exception)
        self.assertGreaterEqual(len(at.get("vega_lite_chart")), 1)


if __name__ == "__main__":
    unittest.main()
