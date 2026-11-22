"""Synthetic-only checks for noise guidance."""

import unittest
from analyzer import analyze
from guidance import find_candidates, next_action_prompt


class GuidanceTests(unittest.TestCase):
    def test_repeated_info_is_candidate_and_error_is_protected(self):
        text = "\n".join(["2026-11-22 10:00:00 INFO connection ready 123"] * 6 +
                         ["2026-11-22 10:00:01 ERROR database failed"])
        result = analyze(text)
        findings = find_candidates(result)
        self.assertEqual(findings[0]["action"], "REVIEW_REDUCE")
        self.assertTrue(any(f["action"] == "PROTECTED" for f in findings))

    def test_audit_info_is_protected(self):
        result = analyze("\n".join(["2026-11-22 10:00:00 INFO audit event 123"] * 5))
        self.assertEqual(find_candidates(result)[0]["action"], "PROTECTED")

    def test_prompt_excludes_real_message_templates(self):
        result = analyze("\n".join(["2026-11-22 10:00:00 INFO PRIVATE-CUSTOMER-XYZ ping 123"] * 5))
        prompt = next_action_prompt(result, find_candidates(result))
        self.assertNotIn("PRIVATE-CUSTOMER-XYZ", prompt)
        self.assertNotIn(result["patterns"][0]["template"], prompt)
        self.assertIn("Find the logging callsite", prompt)

    def test_empty_and_unsupported_input(self):
        report = analyze("unsupported format")
        self.assertEqual(find_candidates(report), [])
        self.assertIn("fix parser coverage", next_action_prompt(report, []))


if __name__ == "__main__":
    unittest.main()
