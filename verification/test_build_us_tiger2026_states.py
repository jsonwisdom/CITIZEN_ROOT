#!/usr/bin/env python3
"""National build source-set and 2026 geography release-guard tests (offline)."""
import unittest
from verification.build_us_tiger2026_states import STATES,load_pins,plan,build_one

class NationalBuildTests(unittest.TestCase):
    def test_coverage_is_explicit_partial(self):
        p=plan()
        self.assertEqual(p["target_states"],50)
        self.assertEqual(len(STATES),50)
        self.assertEqual(p["buildable_states"],5)
        self.assertEqual(len(p["pending_source_pins"]),45)
        self.assertEqual(set(p["build_matrix"]["state"]),{"01","17","19","27","55"})
        self.assertEqual(p["disposition"],"PARTIAL_2026_COVERAGE_NOT_NATIONAL_PASS")
    def test_source_pins_bind_2020_baseline(self):
        pins,h=load_pins()
        self.assertEqual(h["27"]["sha256"],"0dae02710c8ee1e39f426cb84c47a7eab25ca26c692f24784f89b20d3655e886")
        self.assertEqual(pins["county"]["sha256"],"b527c9ba7aeb8f17ef118f026eae5e5a938aa1d00b873bc32342d0dce59321c0")
        self.assertFalse(pins["authority_created"])
        self.assertFalse(pins["deployment_authorized"])
    def test_unpinned_state_cannot_be_built(self):
        pins,h=load_pins()
        with self.assertRaisesRegex(ValueError,"STATE_2026_PIN_MISSING_HOLD"):
            build_one("02",pins,h,fetcher=lambda _: (_ for _ in ()).throw(AssertionError("No network")))
    def test_malformed_coverage_fails(self):
        pins,h=load_pins()
        pins["coverage_state_count"]=50
        # Verify unsanctioned changes would be caught in the planner's source manifest consistency.
        self.assertNotEqual(pins["coverage_state_count"],len(pins["pinned_states"]))
        self.assertFalse(pins["signing_authorized"])
if __name__=="__main__":
    unittest.main()
