#!/usr/bin/env python3
"""Deterministic negative/positive tests; all synthetic bytes, no wallet or secrets."""
import hashlib
import unittest
from verification.import_census_place_county import (
    FIELDS, MN_2020_URL, import_bytes, canonical, read_official_source)

def source(rows):
    head = "|".join(FIELDS)
    return ("\n".join([head] + ["|".join(row) for row in rows]) + "\n").encode("utf-8")

def r(county, name, place, placename, typ="INCORPORATED PLACE"):
    return ["MN", "27", county, name, place, "02395345", placename, typ, "C5", "A"]

class CensusImporterTests(unittest.TestCase):
    def setUp(self):
        self.raw = source([r("053", "Hennepin County", "43000", "Minneapolis city"),
                           r("003", "Anoka County", "06382", "Blaine city"),
                           r("123", "Ramsey County", "06382", "Blaine city")])
        self.sha = hashlib.sha256(self.raw).hexdigest()

    def parse(self, raw=None, sha=None):
        return import_bytes(self.raw if raw is None else raw, source_url=MN_2020_URL,
                            vintage="2020", expected_sha256=self.sha if sha is None else sha)

    def test_provenance_source_bound_and_stable(self):
        output = self.parse()
        self.assertEqual(output["source"]["raw_sha256"], self.sha)
        self.assertEqual(output["source"]["raw_bytes"], len(self.raw))
        self.assertEqual(output["source"]["record_count"], 3)
        self.assertEqual(output["edge_count"], 3)
        self.assertEqual(canonical(output), canonical(self.parse()))
        self.assertIs(output["authority"], False)
        self.assertIsNone(output["wallet_signature"])

    def test_many_to_many_not_one_parent(self):
        out = self.parse()
        self.assertEqual(out["multicounty_place_count"], 1)
        self.assertEqual({x["county_geoid"] for x in out["edges"] if x["place_geoid"] == "2706382"},
                         {"27003", "27123"})
        self.assertEqual({x["county_geoid"] for x in out["edges"] if x["place_geoid"] == "2743000"},
                         {"27053"})

    def test_tamper_and_duplicate_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_SHA256_MISMATCH"):
            self.parse(raw=self.raw.replace(b"Minneapolis", b"Fakeapolis"))
        with self.assertRaisesRegex(ValueError, "DUPLICATE_PLACE_COUNTY_EDGE"):
            raw = source([r("053", "Hennepin County", "43000", "Minneapolis city")] * 2)
            self.parse(raw=raw, sha=hashlib.sha256(raw).hexdigest())

    def test_identifier_and_schema_fail_closed(self):
        for raw in (self.raw.replace(b"|27|", b"|99|", 1),
                    self.raw.replace(b"|06382|", b"|0682|", 1),
                    self.raw.replace(b"COUNTYFP", b"COUNTYX", 1)):
            with self.assertRaises(ValueError):
                self.parse(raw=raw, sha=hashlib.sha256(raw).hexdigest())

    def test_network_allowlist(self):
        with self.assertRaisesRegex(ValueError, "NETWORK_SOURCE_NOT_ALLOWLISTED"):
            read_official_source("https://example.com/fake")

if __name__ == "__main__":
    unittest.main()
