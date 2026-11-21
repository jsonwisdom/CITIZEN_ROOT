#!/usr/bin/env python3
"""BAS candidate match negative/positive tests; synthetic bytes only."""
import hashlib
import unittest
from verification.match_mn_bas_2021_2025 import FIELDS, TARGETS, parse

def sample(geoid="2709730",name="Cannon Falls city",county="049"):
    row={key:"" for key in FIELDS}
    row.update({"BAS ID":"123","GEOID":geoid,"GCATOID":"mock",
       "Entity Name and LSAD":name,"Entity FIPS Code":geoid[2:],
       "County FIPS Code":county,"County Name":"Goodhue",
       "Action":"A","Authorization Type":"O","Local Effective Number":"374",
       "Local Effective Date":"03-16-2021","Keying Date":"04-26-2022",
       "State USPS":"MN","State FIPS":"27","State Name":"Minnesota"})
    return ("\t".join(FIELDS)+"\n"+"\t".join(row[x] for x in FIELDS)+"\n").encode()
def source(raw):
    return {"year":2022,"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),
       "url":"https://www2.census.gov/geo/pvs/bas/annexation/27/27MN_bas2022.txt"}
class Tests(unittest.TestCase):
    def test_candidate_is_not_causation(self):
        raw=sample()
        count,rows=parse(raw,source(raw))
        self.assertEqual(count,1)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["place_geoid"],"2709730")
        self.assertEqual(rows[0]["match_status"],"SAME_GEOID_CANDIDATE_NO_DELTA_CAUSATION")
        self.assertEqual(rows[0]["document_number"],"374")
    def test_hash_fail_closed(self):
        raw=sample()
        with self.assertRaisesRegex(ValueError,"BAS_SOURCE_HASH_OR_SIZE_FAIL"):
            parse(raw+b"!",source(raw))
    def test_changed_schema_fails(self):
        raw=sample().replace(b"GCATOID",b"BADCODE")
        with self.assertRaisesRegex(ValueError,"BAS_SCHEMA_CHANGED"):
            parse(raw,source(raw))
    def test_conflicted_geoid_fails(self):
        raw=sample().replace(b"\t09730\t049",b"\t99999\t049")
        with self.assertRaisesRegex(ValueError,"BAS_IDENTIFIER_CONFLICT"):
            parse(raw,source(raw))
    def test_non_target_does_not_match(self):
        raw=sample(geoid="2700001")
        count,rows=parse(raw,source(raw))
        self.assertEqual(count,1)
        self.assertEqual(rows,[])
if __name__=="__main__":
    unittest.main()
