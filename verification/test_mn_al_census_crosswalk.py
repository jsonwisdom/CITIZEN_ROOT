#!/usr/bin/env python3
"""Strict Minnesota AL legacy-code ↔ Census GEOID crosswalk tests. Synthetic edges only."""
import json
from pathlib import Path
import unittest
BASE = Path(__file__).resolve().parents[1]
PATH = BASE / "jurisdictions/MN_AL_CENSUS_2026_CROSSWALK_V0_1.json"

class MinnesotaCrosswalkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text(encoding="utf-8"))
        cls.items = {x["legacy_code"]: x for x in cls.data["mapping"]}

    def test_source_preserved_and_authority_bounded(self):
        self.assertIs(self.data["source"]["source_bytes_modified"], False)
        self.assertIs(self.data["authority"], False)
        self.assertTrue(self.data["geographic_relationships_can_be_many_to_many"])
        self.assertEqual(self.data["wallet_status"], "HOLD")
        self.assertEqual(self.data["zk_status"], "HOLD")

    def test_census_geoid_widths_and_uniqueness(self):
        self.assertEqual(len(self.items), 5)
        seen = set()
        for row in self.items.values():
            geoid = row["census_geoid"]
            self.assertTrue(geoid.isascii() and geoid.isdigit())
            self.assertEqual(len(geoid), {"state": 2, "county": 5,
                                          "place": 7}[row["census_geoid_kind"]])
            self.assertTrue(geoid.startswith(row["state_fips"]))
            if row["county_fips"] is not None:
                self.assertEqual(geoid, row["state_fips"] + row["county_fips"])
            if row["place_fips"] is not None:
                self.assertEqual(geoid, row["state_fips"] + row["place_fips"])
            self.assertNotIn(geoid, seen)
            seen.add(geoid)

    def test_legacy_numeric_conflicts_flagged_no_silent_rewrite(self):
        expected = {"MN027_HENNEPIN": ("027", "053"),
                    "MN019_DAKOTA": ("019", "037"),
                    "MN062_RAMSEY": ("062", "123")}
        for legacy, (old, official) in expected.items():
            row = self.items[legacy]
            self.assertEqual(row["id_status"], "LEGACY_NUMERIC_CONFLICT")
            self.assertEqual(row["legacy_embedded_numeric"], old)
            self.assertEqual(row["county_fips"], official)
            self.assertNotEqual(old, official)

    def test_minneapolis_edge_not_falsely_attested(self):
        mpls = self.items["MNCI_MPLS"]
        self.assertEqual(mpls["census_geoid"], "2743000")
        self.assertEqual(mpls["relationship_status"], "PLACE_COUNTY_RELATIONSHIP_HOLD")
        edges = self.data["edges"]
        self.assertTrue(any(x["from"] == "2743000" and x["to"] == "27" for x in edges))
        self.assertFalse(any(x["from"] == "2743000" and x["to"] in ("27053", "27037", "27123") for x in edges))
        self.assertTrue(all(x["status"] == "CENSUS_VERIFIED" for x in edges))

if __name__ == "__main__":
    unittest.main()
