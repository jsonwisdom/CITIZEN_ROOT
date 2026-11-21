#!/usr/bin/env python3
"""Nationwide 2026 state build lane, 50-state target / partial coverage explicit.

Strictly pinned official 2020 and 2026 sources. No deployments or signatures.
Runs independently by state, preserving multi-county memberships as sets.
"""
import argparse
import hashlib
import json
from pathlib import Path
from collections import defaultdict

from verification.import_census_place_county import import_bytes
from verification.replay_mn_tiger2026_spatial import shapefile_records,intersection_receipt
from verification.replay_wi_2020_2026_delta_bas import download as fetch_pinned

ROOT=Path(__file__).resolve().parents[1]
PINFILE=ROOT/"jurisdictions/US_TIGER2026_PLACE_SOURCE_PIN_COVERAGE_V0_1.json"
HISTFILE=ROOT/"jurisdictions/US_CENSUS_PLACE_BY_COUNTY_2020_SHA256_MANIFEST.json"
STATES=frozenset("01 02 04 05 06 08 09 10 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56".split())

def load_pins():
    pins=json.loads(PINFILE.read_text())
    hist=json.loads(HISTFILE.read_text())
    if (pins["schema"]!="cw-us-tiger2026-pinned-place-source-coverage-v0.1"
        or pins["vintage"]!=2026 or pins["expected_states"]!=50
        or pins["not_nationwide_complete"] is not True
        or pins["authority_created"] is not False
        or hist["file_count"]!=56):
        raise ValueError("UNTRUSTED_COVERAGE_SCHEMA")
    entries=pins["pinned_states"]
    fips=[e["state_fips"] for e in entries]
    if (len(set(fips))!=len(fips) or not set(fips).issubset(STATES)
        or pins["coverage_state_count"]!=len(entries)
        or pins["remaining_unpinned_states"]!=50-len(entries)):
        raise ValueError("INCOMPLETE_OR_FALSE_COVERAGE")
    county=pins["county"]
    if county["url"]!="https://www2.census.gov/geo/tiger/TIGER2026/COUNTY/tl_2026_us_county.zip":
        raise ValueError("COUNTY_SOURCE_NOT_PINNED")
    for item in entries:
        expected=f'https://www2.census.gov/geo/tiger/TIGER2026/PLACE/tl_2026_{item["state_fips"]}_place.zip'
        if item["url"]!=expected:
            raise ValueError("STATE_PLACE_SOURCE_NOT_PINNED")
    h={x["state_fips"]:x for x in hist["observations"] if x["state_fips"] in STATES}
    if len(h)!=50:
        raise ValueError("HISTORICAL_50_STATE_COVERAGE_MISSING")
    return pins,h

def diff_state(old_edges,current_edges,fips):
    def to_sets(edges):
        result=defaultdict(set)
        for e in edges:
            p,c=e["place_geoid"],e["county_geoid"]
            if (not isinstance(p,str) or not isinstance(c,str)
                or len(p)!=7 or len(c)!=5 or not p.isascii() or not c.isascii()
                or not p.isdigit() or not c.isdigit()
                or not p.startswith(fips) or not c.startswith(fips)):
                raise ValueError("STATE_EDGE_INVALID:"+fips)
            if c in result[p]:
                raise ValueError("DUPLICATE_EDGE")
            result[p].add(c)
        return result
    old=to_sets(old_edges)
    new=to_sets(current_edges)
    counts={k:0 for k in ("UNCHANGED_COUNTY_SET","COUNTY_SET_CHANGED",
         "NEW_IN_2026_EXTRACT","ABSENT_FROM_2026_EXTRACT")}
    changed=[]
    for geoid in sorted(set(old)|set(new)):
        a=old.get(geoid,set())
        b=new.get(geoid,set())
        label=("NEW_IN_2026_EXTRACT" if geoid not in old else
               "ABSENT_FROM_2026_EXTRACT" if geoid not in new else
               "UNCHANGED_COUNTY_SET" if a==b else "COUNTY_SET_CHANGED")
        counts[label]+=1
        if label!="UNCHANGED_COUNTY_SET":
            changed.append({"place_geoid":geoid,"classification":label,
                "before_counties":sorted(a),"after_counties":sorted(b),
                "added_counties":sorted(b-a),"removed_counties":sorted(a-b),
                "bas_legal_causation":"HOLD"})
    return counts,changed

def build_one(fips, pins=None,historical=None, fetcher=fetch_pinned):
    if pins is None or historical is None:
        pins,historical=load_pins()
    candidates=[s for s in pins["pinned_states"] if s["state_fips"]==fips]
    if len(candidates)!=1:
        raise ValueError("STATE_2026_PIN_MISSING_HOLD:"+fips)
    place=candidates[0]
    county=pins["county"]
    old=historical[fips]
    old_url="https://www2.census.gov/geo/docs/reference/codes2020/place_by_cou/"+old["filename"]
    old_src={"url":old_url,"bytes":old["bytes"],"sha256":old["sha256"]}
    baseline=import_bytes(fetcher(old_src),source_url=old_url,vintage="2020",expected_sha256=old["sha256"],expected_state=fips)
    shape_place=shapefile_records(fetcher(place),"place")
    shape_county=shapefile_records(fetcher(county),"county")
    cities=[]
    for rec in shape_place.iterShapeRecords():
        d=rec.record.as_dict()
        if d["STATEFP"]!=fips or d["GEOID"]!=fips+d["PLACEFP"]:
            raise ValueError("INVALID_2026_PLACE_ID")
        cities.append((d["GEOID"],rec.shape.__geo_interface__))
    counties=[]
    for rec in shape_county.iterShapeRecords():
        d=rec.record.as_dict()
        if d["STATEFP"]==fips:
            if d["GEOID"]!=fips+d["COUNTYFP"]:
                raise ValueError("INVALID_2026_COUNTY_ID")
            counties.append((d["GEOID"],rec.shape.__geo_interface__))
    edges=intersection_receipt(cities,counties)
    counts,changes=diff_state(baseline["edges"],edges,fips)
    counts_total=sum(counts.values())
    if counts_total != len({x["place_geoid"] for x in baseline["edges"]}|{x["place_geoid"] for x in edges}):
        raise ValueError("NON_DETERMINISTIC_DIFF_COVERAGE")
    byplace=defaultdict(set)
    for edge in edges:
        byplace[edge["place_geoid"]].add(edge["county_geoid"])
    return {"schema":"cw-national-2026-state-build-receipt-v0.1",
        "state_fips":fips,"source_vintages":[2020,2026],
        "sources":[{"role":"historical","url":old_url,"sha256":old["sha256"]},
                   {"role":"places","url":place["url"],"sha256":place["sha256"]},
                   {"role":"counties","url":county["url"],"sha256":county["sha256"]}],
        "county_count":len(counties),"place_count":len(cities),
        "historical_edges":baseline["edge_count"],"current_edges":len(edges),
        "multicounty_places":sum(len(c)>1 for c in byplace.values()),
        "delta_counts":counts,"changed_places":changes,
        "historical_geography_only":False,"legal_causation_verified":False,
        "signed":False,"deployed":False,"status":"GEOGRAPHY_CI_PASS_LEGAL_CAUSATION_HOLD"}

def plan():
    pins,_=load_pins()
    selected=sorted(x["state_fips"] for x in pins["pinned_states"])
    return {"target_states":50,"buildable_states":len(selected),
            "pending_source_pins":sorted(STATES-set(selected)),
            "build_matrix":{"state":selected},
            "disposition":"PARTIAL_2026_COVERAGE_NOT_NATIONAL_PASS" if len(selected)<50 else "READY_TO_VERIFY_ALL_50"}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--plan",action="store_true")
    parser.add_argument("--state",choices=sorted(STATES))
    parser.add_argument("--out")
    args=parser.parse_args()
    if args.plan:
        print(json.dumps(plan(),sort_keys=True,separators=(",",":")))
        return
    if not args.state:
        parser.error("Use --plan or --state (exactly one)")
    result=build_one(args.state)
    data=(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n").encode()
    if args.out:
        dest=Path(args.out)
        if dest.exists():
            raise SystemExit("OUTPUT_ALREADY_EXISTS")
        dest.write_bytes(data)
    print("CW_STATE_2026_CI_PASS state=%s places=%d counties=%d current_edges=%d multicounty=%d changed=%d receipt_sha256=%s" %
          (args.state,result["place_count"],result["county_count"],result["current_edges"],
           result["multicounty_places"],len(result["changed_places"]),hashlib.sha256(data).hexdigest()))

if __name__=="__main__":
    main()
