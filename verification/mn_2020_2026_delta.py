#!/usr/bin/env python3
"""Census MN 2020↔2026 jurisdiction-edge change ledger v0.1.

Exactly matched place GEOIDs; county membership compared as sets. 2020 source is
Census place_by_cou codes, while 2026 is polygon positive-area intersection.
Differences are OBSERVATIONS, never alleged annexations or legal findings.
"""
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from verification.import_census_place_county import (
    MN_2020_URL, MN_2020_SHA256, import_bytes, read_official_source)
from verification.replay_mn_tiger2026_spatial import run as replay_spatial

SCHEMA="cw-mn-geography-2020-2026-delta-v0.1"

def grouping(edges):
    groups=defaultdict(set)
    names={}
    for edge in edges:
        place=edge["place_geoid"]
        county=edge["county_geoid"]
        if not (len(place)==7 and place.isascii() and place.isdigit() and
                len(county)==5 and county.isascii() and county.isdigit() and
                place.startswith("27") and county.startswith("27")):
            raise ValueError("GEOGRAPHY_ID_INVALID")
        if county in groups[place]:
            raise ValueError("DUPLICATE_PLACE_COUNTY_EDGE")
        groups[place].add(county)
        if "place_name" in edge:
            if place in names and names[place] != edge["place_name"]:
                raise ValueError("AMBIGUOUS_PLACE_NAME")
            names[place]=edge["place_name"]
    if not groups:
        raise ValueError("EMPTY_RELATIONSHIPS")
    return groups,names

def compare(baseline, current, baseline_sha, current_sources):
    if baseline.get("source",{}).get("raw_sha256") != baseline_sha:
        raise ValueError("BASELINE_SOURCE_HASH_NOT_BOUND")
    if baseline.get("state_fips")!="27" or current.get("state")!="27":
        raise ValueError("STATE_SCOPE_MISMATCH")
    if current.get("vintage")!=2026 or current.get("geography_verified") is not True:
        raise ValueError("CURRENT_GEOMETRY_NOT_VERIFIED")
    if baseline.get("source",{}).get("vintage")!="2020":
        raise ValueError("HISTORICAL_VINTAGE_MISMATCH")
    if current.get("sources")!=current_sources:
        raise ValueError("CURRENT_SOURCE_PINS_NOT_BOUND")
    old,names=grouping(baseline["edges"])
    new,_=grouping(current["edges"])
    changes=[]
    for geoid in sorted(set(old)|set(new)):
        before=sorted(old.get(geoid,set()))
        after=sorted(new.get(geoid,set()))
        added=sorted(set(after)-set(before))
        removed=sorted(set(before)-set(after))
        if geoid not in old:
            label="NEW_IN_2026_EXTRACT"
        elif geoid not in new:
            label="ABSENT_FROM_2026_EXTRACT"
        elif added or removed:
            label="COUNTY_SET_CHANGED"
        else:
            label="UNCHANGED_COUNTY_SET"
        changes.append({"place_geoid":geoid,"historical_name":names.get(geoid),
                        "classification":label,"before_county_geoids":before,
                        "after_county_geoids":after,"added_counties":added,
                        "removed_counties":removed,
                        "evidence_status":"GEOGRAPHIC_DELTA_ONLY_BAS_LEGAL_CAUSE_HOLD" if label!="UNCHANGED_COUNTY_SET" else "GEOGRAPHIC_SET_MATCH",
                        "bas_legal_event":None})
    counts={k:sum(x["classification"]==k for x in changes)
            for k in ("NEW_IN_2026_EXTRACT","ABSENT_FROM_2026_EXTRACT","COUNTY_SET_CHANGED","UNCHANGED_COUNTY_SET")}
    return {"schema":SCHEMA,"place_count":len(changes),
            "source_2020":{"url":baseline["source"]["url"],"sha256":baseline_sha,"vintage":2020,
                           "edge_count":baseline["edge_count"]},
            "source_2026":{"vintage":2026,"method":current["method"],
                           "sources":current_sources,"edge_count":current["edge_count"]},
            "counts":counts,"deltas":changes,"legal_change_claimed":False,
            "bas_legal_causation_verified":False,"authority_created":False,
            "wallet_signed":False,"production_release":"HOLD",
            "disposition":"GEOGRAPHIC_DIFF_ONLY_BAS_LEGAL_CHANGE_REPLAY_HOLD"}

def run():
    raw=read_official_source()
    old=import_bytes(raw,source_url=MN_2020_URL,vintage="2020",
                     expected_sha256=MN_2020_SHA256)
    current=replay_spatial()
    return compare(old,current,MN_2020_SHA256,current["sources"])

if __name__=="__main__":
    result=run()
    raw=json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()+b"\n"
    path=Path("mn-2020-2026-geographic-deltas.json")
    if path.exists():
        raise SystemExit("OUTPUT_EXISTS_FAIL_CLOSED")
    path.write_bytes(raw)
    print("CW_MN_2020_2026_GEOGRAPHIC_DELTA_PASS counts=%s sha256=%s"%
          (json.dumps(result["counts"],sort_keys=True,separators=(",",":")),hashlib.sha256(raw).hexdigest()))
