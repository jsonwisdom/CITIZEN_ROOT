#!/usr/bin/env python3
"""Synthetic geometry regression tests. Never promote geographic authority."""
import unittest
from shapely.geometry import box, mapping
from verification.replay_mn_tiger2026_spatial import intersection_receipt, pinned_bytes

class SpatialTests(unittest.TestCase):
    def test_multicounty_place_keeps_both_edges(self):
        counties=[("27003",mapping(box(0,0,1,2))),("27123",mapping(box(1,0,2,2)))]
        places=[("2706382",mapping(box(.5,.5,1.5,1.5)))]
        output=intersection_receipt(places,counties)
        self.assertEqual([x["county_geoid"] for x in output],["27003","27123"])

    def test_touching_boundary_not_area(self):
        counties=[("27003",mapping(box(0,0,1,2))),("27123",mapping(box(1,0,2,2)))]
        output=intersection_receipt([("2706382",mapping(box(0,0,1,1)))],counties)
        self.assertEqual([x["county_geoid"] for x in output],["27003"])

    def test_orphan_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"PLACE_WITHOUT_COUNTY_INTERSECTION"):
            intersection_receipt([("2743000",mapping(box(5,5,6,6)))],[("27053",mapping(box(0,0,1,1)))])

    def test_source_hash_tamper_fails(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_ZIP_SHA256_OR_LENGTH_MISMATCH"):
            pinned_bytes(b"not a zip",{"bytes":9,"sha256":"0"*64})

if __name__=="__main__":
    unittest.main()
