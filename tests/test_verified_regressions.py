import json
import unittest
from memory_safety_lab.auditor import audit_session
class SerializationTests(unittest.TestCase):
    def test_export_never_repeats_detected_sensitive_original(self):
        for value in ('person@example.com', 'api_key_1234567890abcdef', 'cookie=session-private-example'):
            with self.subTest(value=value):
                audit = audit_session({'memory_candidates': ['Remember '+value]})
                self.assertNotIn(value, json.dumps(audit.to_dict()))
                self.assertEqual(audit.memory_candidates[0].text, 'Remember '+value)
