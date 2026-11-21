#!/usr/bin/env python3
"""Synthetic temporal county-set delta tests. No legal causation inferred."""
import unittest
from verification.mn_2020_2026_delta import compare, grouping, SCHEMA
BASE="a"*64
SOURCES=[{"kind":"place","url":"official/p","bytes":2,"sha256":"b"*64},{"kind":"county","url":"official/c","bytes":3,"sha256":"c"*64}]

def old(edges):
    return {"source":{"url":"census/2020","raw_sha256":BASE,"vintage":"2020"},
            "state_fips":"27","edge_count":len(edges),"edges":[
            {"place_geoid":p,"county_geoid":c,"place_name":n} for p,c,n in edges]}

def now(edges):
    return {"state":"27","vintage":2026,"geography_verified":True,
            "method":"synthetic polygon overlap","sources":SOURCES,
            "edge_count":len(edges),
            "edges":[{"place_geoid":p,"county_geoid":c} for p,c in edges]}

class TestTemporalDelta(unittest.TestCase):
    def test_classifications_and_multicounty_sets(self):
        historical=old([("2743000","27053","Minneapolis city"),
                        ("2706382","27003","Blaine city"),
                        ("2706382","27123","Blaine city"),
                        ("2700001","27001","Removed place"),
                        ("2700002","27001","Changed place")])
        latest=now([("2743000","27053"),("2706382","27003"),
                    ("2706382","27123"),("2700002","27003"),
                    ("2700003","27005")])
        out=compare(historical,latest,BASE,SOURCES)
        self.assertEqual(out["schema"],SCHEMA)
        self.assertEqual(out["counts"],{"NEW_IN_2026_EXTRACT":1,
                        "ABSENT_FROM_2026_EXTRACT":1,"COUNTY_SET_CHANGED":1,
                        "UNCHANGED_COUNTY_SET":2})
        change=next(x for x in out["deltas"] if x["place_geoid"]=="2700002")
        self.assertEqual(change["added_counties"],["27003"])
        self.assertEqual(change["removed_counties"],["27001"])
        self.assertIsNone(change["bas_legal_event"])
        self.assertFalse(out["bas_legal_causation_verified"])
        self.assertFalse(out["authority_created"])
        self.assertFalse(out["wallet_signed"])

    def test_one_added_county_preserved_not_single_parent(self):
        first=old([("2706382","27003","Blaine city")])
        second=now([("2706382","27003"),("2706382","27123")])
        result=compare(first,second,BASE,SOURCES)
        item=result["deltas"][0]
        self.assertEqual(item["added_counties"],["27123"])
        self.assertEqual(item["before_county_geoids"],["27003"])
        self.assertEqual(item["after_county_geoids"],["27003","27123"])

    def test_unchanged_multiparent_is_stable(self):
        e=old([("2706382","27123","Blaine city"),("2706382","27003","Blaine city")])
        n=now([("2706382","27003"),("2706382","27123")])
        a=compare(e,n,BASE,SOURCES)
        self.assertEqual(a["counts"]["UNCHANGED_COUNTY_SET"],1)
        self.assertEqual(a["deltas"][0]["classification"],"UNCHANGED_COUNTY_SET")

    def test_duplicate_and_malformed_fail(self):
        with self.assertRaisesRegex(ValueError,"DUPLICATE_PLACE_COUNTY_EDGE"):
            grouping([{"place_geoid":"2743000","county_geoid":"27053"}]*2)
        with self.assertRaisesRegex(ValueError,"GEOGRAPHY_ID_INVALID"):
            grouping([{"place_geoid":"bad","county_geoid":"27053"}])

    def test_provenance_and_vintage_fail_closed(self):
        b=old([("2743000","27053","Minneapolis city")])
        c=now([("2743000","27053")])
        with self.assertRaisesRegex(ValueError,"BASELINE_SOURCE_HASH_NOT_BOUND"):
            compare(b,c,"0"*64,SOURCES)
        with self.assertRaisesRegex(ValueError,"CURRENT_SOURCE_PINS_NOT_BOUND"):
            compare(b,c,BASE,[])
        c["vintage"]=2025
        with self.assertRaisesRegex(ValueError,"CURRENT_GEOMETRY_NOT_VERIFIED"):
            compare(b,c,BASE,SOURCES)

if __name__=="__main__":
    unittest.main()
