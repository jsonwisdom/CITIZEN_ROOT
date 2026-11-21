#!/usr/bin/env python3
"""Wisconsin 2020→2026 synthetic deltas; no BAS causation inferred."""
import hashlib
import unittest
from verification.replay_wi_2020_2026_delta_bas import diff,bas_candidate_rows,verify_bytes,BAS_HEADER

class WisconsinTests(unittest.TestCase):
    def test_multicounty_set_delta_and_preservation(self):
        old=[{"place_geoid":"5502380","county_geoid":c} for c in ("55015","55087")]
        now=old+[{"place_geoid":"5502380","county_geoid":"55139"}]
        counts,changes=diff(old,now)
        self.assertEqual(counts["COUNTY_SET_CHANGED"],1)
        self.assertEqual(changes[0]["added"],["55139"])
        self.assertEqual(changes[0]["before_counties"],["55015","55087"])
        self.assertEqual(changes[0]["after_counties"],["55015","55087","55139"])
        self.assertEqual(changes[0]["bas_causation"],"HOLD")

    def test_new_absent_and_unchanged(self):
        a=[{"place_geoid":"5500001","county_geoid":"55001"},
           {"place_geoid":"5500002","county_geoid":"55003"}]
        b=[{"place_geoid":"5500002","county_geoid":"55003"},
           {"place_geoid":"5500003","county_geoid":"55005"}]
        counts,_=diff(a,b)
        self.assertEqual(counts,{"UNCHANGED_COUNTY_SET":1,"COUNTY_SET_CHANGED":0,
           "NEW_IN_2026_EXTRACT":1,"ABSENT_FROM_2026_EXTRACT":1})

    def test_duplicate_and_cross_state_fail_closed(self):
        edge={"place_geoid":"5500001","county_geoid":"55001"}
        with self.assertRaisesRegex(ValueError,"DUPLICATE_EDGE"):
            diff([edge,edge],[edge])
        with self.assertRaisesRegex(ValueError,"STATE_EDGE_INVALID"):
            diff([{"place_geoid":"2700001","county_geoid":"27001"}],[edge])

    def test_source_tamper(self):
        data=b"source"
        source={"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
        self.assertEqual(verify_bytes(data,source),data)
        with self.assertRaisesRegex(ValueError,"SOURCE_SIZE_OR_SHA256_FAIL"):
            verify_bytes(data+b"x",source)

    def test_bas_candidate_no_causation(self):
        row={k:"" for k in BAS_HEADER}
        row.update({"State FIPS":"55","State USPS":"WI","GEOID":"5500001",
           "Entity FIPS Code":"00001","County FIPS Code":"001",
           "BAS ID":"1","GCATOID":"2","Action":"A",
           "Local Effective Number":"999","Local Effective Date":"01-02-2022"})
        data=("\t".join(BAS_HEADER)+"\n"+"\t".join(row[x] for x in BAS_HEADER)+"\n").encode()
        n,m=bas_candidate_rows(data,{"year":2022,"sha256":hashlib.sha256(data).hexdigest()},{"5500001"})
        self.assertEqual(n,1)
        self.assertEqual(m[0]["status"],"SAME_GEOID_CANDIDATE_CAUSATION_HOLD")
        self.assertEqual(m[0]["effective_number"],"999")

if __name__=="__main__":
    unittest.main()
