"""Unit tests that run without Streamlit or network access."""

import unittest
from datetime import datetime, timezone

from analyzer import MAX_BYTES, analyze, normalize_message, parse_line, to_markdown


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

    def test_limits_and_empty_input(self):
        self.assertEqual(analyze("")["matched_lines"], 0)
        with self.assertRaises(ValueError):
            analyze("x" * (MAX_BYTES + 1))
        self.assertIsNone(parse_line("nonsense"))


if __name__ == "__main__":
    unittest.main()
