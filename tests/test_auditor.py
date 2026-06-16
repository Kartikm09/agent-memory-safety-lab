import json
import unittest
from pathlib import Path

from memory_safety_lab.auditor import audit_session
from memory_safety_lab.patterns import detect, redact


ROOT = Path(__file__).resolve().parents[1]


class MemorySafetyTests(unittest.TestCase):
    def test_example_has_mixed_decisions(self):
        payload = json.loads((ROOT / "examples" / "session.json").read_text())
        audit = audit_session(payload)
        self.assertEqual(audit.summary["allow"], 4)
        self.assertEqual(audit.summary["redact"], 1)
        self.assertEqual(audit.summary["block"], 1)

    def test_redacts_email(self):
        text = "Reach me at person@example.com."
        self.assertEqual(redact(text), "Reach me at [REDACTED_EMAIL].")
        self.assertEqual(detect(text)[0].label, "email")

    def test_key_blocks_candidate(self):
        payload = {"session_id": "x", "memory_candidates": ["store api_key_1234567890abcdef for next run"]}
        audit = audit_session(payload)
        self.assertEqual(audit.memory_candidates[0].decision, "block")


if __name__ == "__main__":
    unittest.main()
