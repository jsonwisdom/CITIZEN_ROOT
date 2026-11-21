#!/usr/bin/env python3
"""Offline fail-closed tests for Census Gazetteer identity continuity."""
import hashlib
import unittest
from verification.verify_mn_2026_gazetteers import DOC, pinned_rows, run
import json

class TestGazetteer(unittest.TestCase):
    def setUp(self):
        self.doc=json.loads(DOC.read_text())

    def test_pins_and_authority_hold(self):
        self.assertEqual(self.doc["reference_vintage"],2020)
        self.assertEqual(self.doc["current_vintage"],2026)
        self.assertFalse(self.doc["authority"])
        self.assertEqual(self.doc["wallet_signing"],"HOLD")
        self.assertEqual(len(self.doc["sources"]),2)
        self.assertEqual({x["observed_row"]["GEOID"] for x in self.doc["sources"]},{"27053","2743000"})

    def test_offline_parse_and_mutation_rejected(self):
        src=self.doc["sources"][0]
        row=src["observed_row"]
        keys=src["header"].split("|")
        values=[row.get(k,{"ALAND":"1","AWATER":"0","ALAND_SQMI":"1","AWATER_SQMI":"0","INTPTLAT":"1","INTPTLONG":"-1","LSAD":"25","FUNCSTAT":"A"}.get(k,"1")) for k in keys]
        raw=("|".join(keys)+"\n"+"|".join(values)+"\n").encode()
        synthetic={**src,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
        self.assertEqual(pinned_rows(raw,synthetic)["target_geoid"],"2743000")
        with self.assertRaisesRegex(ValueError,"GAZETTEER_HASH_OR_SIZE_DRIFT"):
            pinned_rows(raw+b"tampered",synthetic)
        forged=raw.replace(b"Minneapolis city",b"Fakelapolis city")
        synthetic_bad={**synthetic,"bytes":len(forged),"sha256":hashlib.sha256(forged).hexdigest()}
        with self.assertRaisesRegex(ValueError,"GAZETTEER_TARGET_MISSING_OR_CHANGED"):
            pinned_rows(forged,synthetic_bad)

    def test_absent_source_fails(self):
        with self.assertRaises(KeyError):
            run(source_bytes={})

if __name__=="__main__":
    unittest.main()
