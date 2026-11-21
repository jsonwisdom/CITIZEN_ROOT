#!/usr/bin/env python3
"""CI-FIRST national discovery overlay validator. Read-only, pointer-only, no signing."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "registry/CW_NATIONAL_RECOVERY_OVERLAY_2026_11_21_V0_1.json"

class RecoveryOverlayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = OVERLAY.read_bytes()
        cls.m = json.loads(cls.raw)

    def test_schema_canonical_and_no_promotion(self):
        m = self.m
        self.assertEqual(m["schema"], "cw-national-recovery-overlay-v0.1")
        self.assertEqual(m["disposition"], "DISCOVERY_OVERLAY_ONLY_NO_SOURCE_PROMOTION")
        p = m["policy"]
        for key in ("source_bytes_rewrite_forbidden", "private_repository_names_and_paths_redacted",
                    "secrets_and_wallet_keys_forbidden", "source_git_sha1_is_not_sha256"):
            self.assertIs(p[key], True)
        self.assertEqual(p["signing_status"], "HOLD")
        self.assertIs(p["government_emergency_authority"], False)

    def test_verified_file_pointers_are_unique_and_sha1(self):
        pairs = set()
        for x in self.m["sources"]:
            self.assertRegex(x["repo"], r"^jsonwisdom/[A-Za-z0-9_.-]+$")
            self.assertIsInstance(x["path"], str)
            self.assertTrue(x["path"] and not x["path"].startswith("/") and ".." not in x["path"].split("/"))
            self.assertRegex(x["git_blob_sha1"], r"^[a-f0-9]{40}$")
            self.assertEqual(x["status"], "POINTER_VERIFIED_CONTENT_REPLAY_HOLD")
            self.assertIs(x["authority"], False)
            pair = (x["repo"], x["path"])
            self.assertNotIn(pair, pairs)
            pairs.add(pair)
        self.assertEqual(len(pairs), 15)

    def test_city_county_state_national_and_multicounty_synthetic(self):
        # Distinguish entities from adjacency: a city may cross county boundaries.
        nodes = {"city:synthetic-A", "county:synthetic-1",
                 "county:synthetic-2", "state:synthetic-X", "US"}
        edges = {("city:synthetic-A", "county:synthetic-1"),
                 ("city:synthetic-A", "county:synthetic-2"),
                 ("county:synthetic-1", "state:synthetic-X"),
                 ("county:synthetic-2", "state:synthetic-X"),
                 ("state:synthetic-X", "US")}
        def reach(start, goal, reverse=False):
            todo = [start]
            visited = set()
            while todo:
                u = todo.pop()
                if u == goal:
                    return True
                if u in visited:
                    continue
                visited.add(u)
                todo.extend(b if a == u else a for a,b in edges
                            if (a == u if not reverse else b == u))
            return False
        self.assertTrue(all(a in nodes and b in nodes for a,b in edges))
        self.assertTrue(reach("city:synthetic-A", "US"))
        self.assertTrue(reach("US", "city:synthetic-A", reverse=True))
        self.assertEqual(sum(a == "city:synthetic-A" for a,b in edges), 2)

    def test_geography_does_not_assert_complete_coverage(self):
        self.assertTrue(self.m["geography"]["coverage_counts_are_targets_not_established"])
        self.assertFalse(self.m["inventory_complete_for_all_repositories"])
        self.assertIn("emergency", self.m["missions"])
        self.assertIn("audit", self.m["missions"])

if __name__ == "__main__":
    unittest.main()
