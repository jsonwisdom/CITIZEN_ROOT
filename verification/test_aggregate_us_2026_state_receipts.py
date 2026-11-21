#!/usr/bin/env python3
"""Independent synthetic tests for national evidence root and release gates."""
import hashlib
import json
import unittest
from verification.aggregate_us_2026_state_receipts import (
    merkle_root, leaf, verify_state_receipt, load_pins, NODE_PREFIX)

def fixture():
    fips="01"
    hsha="a"*64
    psha="b"*64
    csha="c"*64
    sources={"pinned_states_by_fips":{"01":{"url":"https://census.test/01.zip","sha256":psha}},
             "county":{"url":"https://census.test/counties.zip","sha256":csha},
             "history_by_fips":{"01":{"filename":"st01_al_place_by_county2020.txt","sha256":hsha}}}
    rec={"schema":"cw-national-2026-state-build-receipt-v0.1",
         "state_fips":"01","source_vintages":[2020,2026],
         "status":"GEOGRAPHY_CI_PASS_LEGAL_CAUSATION_HOLD",
         "legal_causation_verified":False,"signed":False,"deployed":False,
         "sources":[
             {"role":"historical","url":"https://www2.census.gov/geo/docs/reference/codes2020/place_by_cou/st01_al_place_by_county2020.txt","sha256":hsha},
             {"role":"places","url":"https://census.test/01.zip","sha256":psha},
             {"role":"counties","url":"https://census.test/counties.zip","sha256":csha}
         ],
         "place_count":2,"county_count":2,"current_edges":3,
         "multicounty_places":1,"historical_edges":2,
         "delta_counts":{"UNCHANGED_COUNTY_SET":1,"COUNTY_SET_CHANGED":1,
                         "NEW_IN_2026_EXTRACT":0,"ABSENT_FROM_2026_EXTRACT":0},
         "changed_places":[{"place_geoid":"0100002","classification":"COUNTY_SET_CHANGED",
            "before_counties":["01001"],"after_counties":["01001","01003"],
            "added_counties":["01003"],"removed_counties":[],
            "bas_legal_causation":"HOLD"}]}
    raw=(json.dumps(rec,sort_keys=True,separators=(",",":"))+"\n").encode()
    return rec,raw,sources

class AggregateTests(unittest.TestCase):
    def test_fifty_independently_pinned_states(self):
        pins,sources=load_pins()
        self.assertEqual(len(pins["states"]),50)
        self.assertEqual(len(sources["pinned_states_by_fips"]),50)
        self.assertFalse(pins["signing_authorized"])
        self.assertEqual(pins["production_deployment"],"HOLD")

    def test_synthetic_valid_with_original_hash(self):
        rec,raw,sources=fixture()
        self.assertEqual(verify_state_receipt(raw,"01",hashlib.sha256(raw).hexdigest(),sources),rec)

    def test_tampered_source_bytes_are_rejected(self):
        rec,raw,sources=fixture()
        with self.assertRaisesRegex(ValueError,"ORIGINAL_LOG_RECEIPT_SHA256_MISMATCH"):
            verify_state_receipt(raw+b" ","01",hashlib.sha256(raw).hexdigest(),sources)

    def test_changed_government_authority_rejected(self):
        rec,raw,sources=fixture()
        rec["legal_causation_verified"]=True
        new=(json.dumps(rec,sort_keys=True,separators=(",",":"))+"\n").encode()
        with self.assertRaisesRegex(ValueError,"RECEIPT_SCOPE_OR_GATES_INVALID"):
            verify_state_receipt(new,"01",hashlib.sha256(new).hexdigest(),sources)

    def test_set_difference_tamper_rejected(self):
        rec,raw,sources=fixture()
        rec["changed_places"][0]["added_counties"]=[]
        new=(json.dumps(rec,sort_keys=True,separators=(",",":"))+"\n").encode()
        with self.assertRaisesRegex(ValueError,"DELTA_SET_DIFF_INVALID"):
            verify_state_receipt(new,"01",hashlib.sha256(new).hexdigest(),sources)

    def test_merkle_domain_separation_and_order(self):
        x={"55":"a"*64,"01":"b"*64,"27":"c"*64}
        self.assertEqual(merkle_root(x),merkle_root(dict(reversed(list(x.items())))))
        a,b,c=[leaf(s,x[s]) for s in sorted(x)]
        left=hashlib.sha256(NODE_PREFIX+a+b).digest()
        right=hashlib.sha256(NODE_PREFIX+c+c).digest()
        expected=hashlib.sha256(NODE_PREFIX+left+right).hexdigest()
        self.assertEqual(merkle_root(x),expected)
        self.assertNotEqual(merkle_root({"01":"b"*64}),merkle_root({"55":"b"*64}))

if __name__=="__main__":
    unittest.main()
