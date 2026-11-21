#!/usr/bin/env python3
"""2026 Minnesota Census identity continuity; live pins, not spatial membership."""
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "jurisdictions/MN_CENSUS_2020_2026_IDENTITY_COMPARISON_V0_1.json"

def pinned_rows(raw, item):
    if len(raw) != item["bytes"] or hashlib.sha256(raw).hexdigest() != item["sha256"]:
        raise ValueError("GAZETTEER_HASH_OR_SIZE_DRIFT")
    try:
        decoded = raw.decode("utf-8-sig")
    except UnicodeDecodeError as ex:
        raise ValueError("GAZETTEER_NOT_UTF8") from ex
    rows = list(csv.DictReader(io.StringIO(decoded, newline=""), delimiter="|"))
    if not rows or "|".join(rows[0].keys()) != item["header"]:
        raise ValueError("GAZETTEER_SCHEMA_DRIFT")
    ids = set()
    for row in rows:
        if None in row or any(v is None for v in row.values()):
            raise ValueError("GAZETTEER_BAD_RECORD")
        if row["USPS"] != "MN" or not row["GEOID"].startswith("27"):
            raise ValueError("GAZETTEER_OUTSIDE_MINNESOTA")
        if row["GEOID"] in ids:
            raise ValueError("GAZETTEER_DUPLICATE_GEOID")
        ids.add(row["GEOID"])
    expected = item["observed_row"]
    matches = [row for row in rows if row["GEOID"] == expected["GEOID"]]
    if len(matches) != 1 or any(matches[0][key] != value for key,value in expected.items()):
        raise ValueError("GAZETTEER_TARGET_MISSING_OR_CHANGED")
    return {"source_url":item["url"],"raw_sha256":item["sha256"],
            "byte_count":len(raw),"record_count":len(rows),
            "target_geoid":expected["GEOID"],"target_geoidfq":expected["GEOIDFQ"],
            "status":"PASS_IDENTITY_ONLY_SPATIAL_MEMBERSHIP_HOLD"}

def run(*, fetch=False, source_bytes=None):
    doc = json.loads(DOC.read_text())
    if doc["status"] != "PINNED_2026_IDENTIFIER_OBSERVATION_SPATIAL_INTERSECTION_HOLD":
        raise ValueError("UNAUTHORIZED_GEO_PROMOTION")
    out = []
    for source in doc["sources"]:
        if fetch:
            request = urllib.request.Request(source["url"], headers={"Accept-Encoding":"identity"})
            with urllib.request.urlopen(request, timeout=25) as response:
                if response.status != 200 or response.geturl() != source["url"] or response.headers.get("Content-Encoding","identity").lower() != "identity":
                    raise ValueError("GAZETTEER_HTTP_OR_REDIRECT_DRIFT")
                data = response.read(source["bytes"]+1)
        elif source_bytes is not None:
            data = source_bytes[source["type"]]
        else:
            raise ValueError("NO_GAZETTEER_BYTES")
        out.append(pinned_rows(data, source))
    return {"schema":"cw-mn-2026-gazetteer-identity-replay-v0.1",
            "source_vintage":2026,"references_2020":True,"sources":out,
            "current_place_county_membership_verified":False,
            "legal_authority_created":False,"status":"PASS_IDENTITY_ONLY_SPATIAL_HOLD"}

if __name__ == "__main__":
    print(json.dumps(run(fetch=True),sort_keys=True))
