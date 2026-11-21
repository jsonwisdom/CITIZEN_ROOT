#!/usr/bin/env python3
"""Read-only Minnesota BAS 2021-2025 candidate search for 2020↔2026 changed places.

BAS event found by place GEOID is a CANDIDATE ONLY, never legal causation,
proof of annexation, government authority, or proof that missing rows are inactive.
"""
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"jurisdictions/MN_BAS_2021_2025_SHA256_SOURCE_MANIFEST.json"
TARGETS={
    "2703282":"Baldwin city", "2704618":"Becker city",
    "2709730":"Cannon Falls city", "2713708":"Credit River city",
    "2719358":"Empire city", "2743270":"Minnetonka Beach city",
    "2747068":"North Mankato city", "2767130":"Village of Minnetonka Beach city",
}
FIELDS=("BAS ID","GEOID","GCATOID","Entity Name and LSAD","Entity FIPS Code",
        "County FIPS Code","County Name","Action","Authorization Type",
        "Local Effective Number","Secondary Effective Number","Local Effective Date",
        "Secondary Effective Date","Acreage","Keying Date","State USPS",
        "State FIPS","State Name","State Cert Flag")
def parse(raw,src):
    if len(raw)!=src["bytes"] or hashlib.sha256(raw).hexdigest()!=src["sha256"]:
        raise ValueError("BAS_SOURCE_HASH_OR_SIZE_FAIL")
    try:
        decoded=raw.decode("utf-8-sig")
    except UnicodeDecodeError as ex:
        raise ValueError("BAS_INVALID_UTF8") from ex
    reader=csv.DictReader(io.StringIO(decoded,newline=""),delimiter="\t")
    if tuple(reader.fieldnames or ())!=FIELDS:
        raise ValueError("BAS_SCHEMA_CHANGED")
    matches=[]
    total=0
    for r in reader:
        total+=1
        if None in r or any(v is None for v in r.values()):
            raise ValueError("BAS_ROW_INVALID")
        if r["State FIPS"]!="27" or r["State USPS"]!="MN":
            raise ValueError("BAS_WRONG_STATE")
        if r["GEOID"] in TARGETS:
            if r["Entity FIPS Code"]!=r["GEOID"][2:]:
                raise ValueError("BAS_IDENTIFIER_CONFLICT")
            matches.append({
                "place_geoid":r["GEOID"],
                "name_in_bas":r["Entity Name and LSAD"],
                "reported_county_geoid":"27"+r["County FIPS Code"],
                "bas_year":src["year"],
                "source_sha256":src["sha256"],
                "source_url":src["url"],
                "bas_id":r["BAS ID"],
                "gcatoid":r["GCATOID"],
                "action":r["Action"],
                "authorization_type":r["Authorization Type"],
                "document_number":r["Local Effective Number"] or None,
                "reported_effective_date":r["Local Effective Date"] or None,
                "keying_date":r["Keying Date"] or None,
                "match_status":"SAME_GEOID_CANDIDATE_NO_DELTA_CAUSATION"})
    return total,matches

def fetch(src):
    if src["url"]!="https://www2.census.gov/geo/pvs/bas/annexation/27/"+src["filename"]:
        raise ValueError("BAS_UNTRUSTED_SOURCE_URL")
    req=urllib.request.Request(src["url"],headers={"Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=30) as resp:
        if resp.status!=200 or resp.geturl()!=src["url"] or resp.headers.get("Content-Encoding","identity").lower()!="identity":
            raise ValueError("BAS_FETCH_OR_REDIRECT_FAIL")
        data=resp.read(src["bytes"]+1)
    return data

def run(fetcher=fetch):
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    files=manifest["files"]
    if manifest["schema"]!="cw-mn-bas-2021-2025-legal-source-pins-v0.1" or [f["year"] for f in files]!=[2021,2022,2023,2024,2025]:
        raise ValueError("BAS_MANIFEST_INVALID")
    candidates=[]
    counts={}
    for src in files:
        total,hit=parse(fetcher(src),src)
        counts[str(src["year"])]=total
        candidates.extend(hit)
    grouped={geoid:sorted([row for row in candidates if row["place_geoid"]==geoid],key=lambda r:(r["bas_year"],r["bas_id"],r["gcatoid"])) for geoid in sorted(TARGETS)}
    return {"schema":"cw-mn-bas-candidate-links-v0.1","sources":[{"url":s["url"],"sha256":s["sha256"],"year":s["year"]} for s in files],
            "matched_entity_count":sum(bool(rows) for rows in grouped.values()),
            "matched_bas_row_count":len(candidates),"source_row_counts":counts,
            "places":[{"place_geoid":code,"gazetteer_or_historical_name":TARGETS[code],
                       "bas_candidates":grouped[code],
                       "legal_causation":"HOLD"} for code in sorted(TARGETS)],
            "census_2026_spatial_causation_verified":False,"legal_boundary_event_claimed":False,
            "authority_created":False,"wallet_signed":False,
            "disposition":"BAS_ENTITY_MATCH_ONLY_GEO_DELTA_CAUSATION_HOLD"}
if __name__=="__main__":
    result=run()
    data=(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
    target=Path("mn-bas-2021-2025-eight-geoid-candidates.json")
    if target.exists():
        raise SystemExit("OUTPUT_EXISTS")
    target.write_bytes(data)
    print("CW_MN_BAS_CANDIDATES_MATCHED entities=%d rows=%d counts=%s sha256=%s"%
          (result["matched_entity_count"],result["matched_bas_row_count"],
           json.dumps(result["source_row_counts"],sort_keys=True),hashlib.sha256(data).hexdigest()))
    print("CW_MN_BAS_CANDIDATE_SUMMARY="+json.dumps([{"geoid":p["place_geoid"],"name":p["gazetteer_or_historical_name"],"bas_record_count":len(p["bas_candidates"]),"bas_years":sorted(set(c["bas_year"] for c in p["bas_candidates"]))} for p in result["places"]],sort_keys=True,separators=(",",":")))
