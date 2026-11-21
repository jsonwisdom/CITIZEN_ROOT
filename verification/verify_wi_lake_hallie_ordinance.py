#!/usr/bin/env python3
"""CI-FIRST immutable Wisconsin Lake Hallie ordinance PDF source byte verifier.

This verifies exact DOA/MDS PDF only; DOES NOT georeference its legal description,
independently establish annexation geometry, or authorize a legal finding.
"""
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"jurisdictions/WI_LAKE_HALLIE_ORD11315_ORIGINAL_PDF_SHA256_V0_1.json"

def verify(raw,proof):
    pinned=proof["ordinance_exact_bytes"]
    if len(raw)!=pinned["length_bytes"] or hashlib.sha256(raw).hexdigest()!=pinned["sha256"]:
        raise ValueError("ORDINANCE_SOURCE_HASH_OR_SIZE_DRIFT")
    if not raw.startswith(b"%PDF-"):
        raise ValueError("ORDINANCE_NOT_PDF")
    if proof["boundary_parcel_georeferencing"]!="HOLD" or proof["ordinance_polygon_area_intersection_with_2026"]!="HOLD":
        raise ValueError("UNAUTHORIZED_CAUSATION_PROMOTION")
    return {"status":"PDF_BYTES_AND_HASH_PASS_GEOMETRIC_CAUSATION_HOLD",
            "url":proof["original_document_url"],"source_sha256":pinned["sha256"],
            "source_bytes":len(raw),"survey_polygon_verified":False,
            "legal_causation_fully_reconciled":False,"wallet_signed":False}

def run():
    proof=json.loads(MANIFEST.read_text(encoding="utf-8"))
    url="https://mds.wi.gov/View/Documents?ID=11315&Type=OrdinanceFile"
    if proof["schema"]!="cw-wi-lake-hallie-ordinance-byte-proof-v0.1" or proof["original_document_url"]!=url:
        raise ValueError("UNTRUSTED_ORDINANCE_SOURCE")
    req=urllib.request.Request(url,headers={"Accept-Encoding":"identity","User-Agent":"ComputerWisdom-CI-FIRST/0.1"})
    with urllib.request.urlopen(req,timeout=90) as response:
        if response.status!=200 or response.geturl()!=url or response.headers.get("Content-Encoding","identity").lower()!="identity":
            raise ValueError("ORDINANCE_HTTP_OR_REDIRECT_DRIFT")
        raw=response.read(proof["ordinance_exact_bytes"]["length_bytes"]+1)
    return verify(raw,proof)

if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True,separators=(",",":")))
