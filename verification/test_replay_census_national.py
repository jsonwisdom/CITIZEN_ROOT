#!/usr/bin/env python3
"""Synthetic national Census replay CI guards, no outbound network."""
import hashlib
import unittest
from verification.import_census_place_county import FIELDS
from verification.replay_census_national import (
    EXPECTED, OTHER_FIPS, STATE_FIPS, load_manifest, replay_all, replay_one)


def mock_source(fips, rows=1):
    head = "|".join(FIELDS)
    records = []
    for i in range(rows):
        county = "001" if i == 0 else "003"
        records.append("|".join(["ZZ", fips, county, "Synthetic County",
                                 "00001", "00000001", "Synthetic Place",
                                 "INCORPORATED PLACE", "C5", "A"]))
    return ("\n".join([head] + records) + "\n").encode()


class NationwideTests(unittest.TestCase):
    def test_manifest_56_exact_states(self):
        sources = load_manifest()
        self.assertEqual(len(sources), 56)
        self.assertEqual(len(STATE_FIPS), 50)
        self.assertEqual(len(OTHER_FIPS), 6)
        self.assertEqual({s["state_fips"] for s in sources}, EXPECTED)
        self.assertEqual(next(s["sha256"] for s in sources if s["state_fips"] == "27"),
                         "0dae02710c8ee1e39f426cb84c47a7eab25ca26c692f24784f89b20d3655e886")

    def test_cross_state_and_size_tamper_rejected(self):
        sources = load_manifest()
        selected = next(s for s in sources if s["state_fips"] == "27").copy()
        raw = mock_source("27")
        selected["bytes"] = len(raw)
        selected["sha256"] = hashlib.sha256(raw).hexdigest()
        self.assertEqual(replay_one(selected, raw)["edge_count"], 1)
        with self.assertRaises(ValueError):
            replay_one(selected, mock_source("11"))
        with self.assertRaisesRegex(ValueError, "SOURCE_BYTES_CHANGED"):
            replay_one(selected, raw + b"changed")

    def test_all_56_synthetic_and_two_counties(self):
        files = []
        content = {}
        for state in sorted(EXPECTED):
            raw = mock_source(state, rows=2 if state == "27" else 1)
            content[state] = raw
            files.append({"state_fips": state, "filename": f"st{state}_xx_place_by_county2020.txt",
                          "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        result = replay_all(files, downloader=lambda src: content[src["state_fips"]], max_workers=4)
        self.assertEqual(result["state_count"], 50)
        self.assertEqual(result["additional_jurisdiction_count"], 6)
        self.assertEqual(result["file_count"], 56)
        self.assertEqual(result["edges_total"], 57)
        self.assertEqual(result["multicounty_places_total"], 1)
        self.assertFalse(result["legal_authority"])
        self.assertFalse(result["emergency_dispatch_authority"])

    def test_missing_source_fails_closed(self):
        sources = load_manifest()
        with self.assertRaisesRegex(ValueError, "COVERAGE_GAP"):
            replay_all(sources[:-1], downloader=lambda s: b"")

if __name__ == "__main__":
    unittest.main()
