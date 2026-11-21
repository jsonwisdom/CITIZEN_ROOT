#!/usr/bin/env python3
"""Lake Hallie source-document hash and nonpromotion synthetic tests."""
import hashlib
import unittest
from verification.verify_wi_lake_hallie_ordinance import verify

class OrdinanceSourceTests(unittest.TestCase):
    def setUp(self):
        self.raw=b"%PDF-1.7\nSynthetic bytes\n"
        self.proof={"ordinance_exact_bytes":{"sha256":hashlib.sha256(self.raw).hexdigest(),
                    "length_bytes":len(self.raw)},
                    "boundary_parcel_georeferencing":"HOLD",
                    "ordinance_polygon_area_intersection_with_2026":"HOLD",
                    "original_document_url":"https://example.test/ordinance"}
    def test_synthetic_source_hash_and_no_causation(self):
        x=verify(self.raw,self.proof)
        self.assertEqual(x["status"],"PDF_BYTES_AND_HASH_PASS_GEOMETRIC_CAUSATION_HOLD")
        self.assertFalse(x["legal_causation_fully_reconciled"])
        self.assertFalse(x["survey_polygon_verified"])
    def test_tamper_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"ORDINANCE_SOURCE_HASH_OR_SIZE_DRIFT"):
            verify(self.raw+b"x",self.proof)
    def test_non_pdf_fails_closed(self):
        raw=b"not a pdf"
        proof={**self.proof,"ordinance_exact_bytes":{"sha256":hashlib.sha256(raw).hexdigest(),
                "length_bytes":len(raw)}}
        with self.assertRaisesRegex(ValueError,"ORDINANCE_NOT_PDF"):
            verify(raw,proof)
    def test_geometry_promotion_without_evidence_fails(self):
        self.proof["boundary_parcel_georeferencing"]="PASS"
        with self.assertRaisesRegex(ValueError,"UNAUTHORIZED_CAUSATION_PROMOTION"):
            verify(self.raw,self.proof)
if __name__=="__main__":
    unittest.main()
