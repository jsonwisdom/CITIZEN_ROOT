#!/usr/bin/env python3
"""WI 2020↔2026 Census geographic delta + 2021–25 BAS candidates.

Read-only source SHA-256 pins; geographic edges are NOT legal events.
"""
import csv
import hashlib
import io
import json
from collections import defaultdict
from pathlib import Path
import urllib.request

from verification.import_census_place_county import import_bytes
from verification.replay_mn_tiger2026_spatial import shapefile_records, intersection_receipt

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"jurisdictions/WI_CENSUS_2020_2026_BAS_SOURCE_MANIFEST_V0_1.json"
STATE="55"
EXPECTED_KINDS={"2020_place_by_county","2026_places","2026_counties"}
BAS_HEADER=("BAS ID","GEOID","GCATOID","Entity Name and LSAD","Entity FIPS Code",
    "County FIPS Code","County Name","Action","Authorization Type",
    "Local Effective Number","Secondary Effective Number","Local Effective Date",
    "Secondary Effective Date","Acreage","Keying Date","State USPS",
    "State FIPS","State Name","State Cert Flag")

def download(src):
    url=src["url"]
    if not url.startswith("https://www2.census.gov/") or any(x in url for x in ("..","?","#")):
        raise ValueError("SOURCE_NOT_OFFICIAL_OR_UNSAFE")
    req=urllib.request.Request(url,headers={"Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=120) as r:
        if r.status!=200 or r.geturl()!=url or r.headers.get("Content-Encoding","identity").lower()!="identity":
            raise ValueError("HTTP_OR_REDIRECT_DRIFT")
        raw=r.read(src["bytes"]+1)
    return verify_bytes(raw,src)

def verify_bytes(raw,src):
    if len(raw)!=src["bytes"] or hashlib.sha256(raw).hexdigest()!=src["sha256"]:
        raise ValueError("SOURCE_SIZE_OR_SHA256_FAIL")
    return raw

def build_spatial(place_raw,county_raw):
    places=[];counties=[]
    for rec in shapefile_records(place_raw,"place").iterShapeRecords():
        r=rec.record.as_dict()
        if r["STATEFP"]!="55" or r["GEOID"]!="55"+r["PLACEFP"]:
            raise ValueError("PLACE_GEOID_INVALID")
        places.append((r["GEOID"],rec.shape.__geo_interface__))
    for rec in shapefile_records(county_raw,"county").iterShapeRecords():
        r=rec.record.as_dict()
        if r["STATEFP"]=="55":
            if r["GEOID"]!="55"+r["COUNTYFP"]:
                raise ValueError("COUNTY_GEOID_INVALID")
            counties.append((r["GEOID"],rec.shape.__geo_interface__))
    if len(counties)!=72 or not places:
        raise ValueError("WISCONSIN_COUNTY_COUNT_OR_PLACE_MISSING")
    edges=intersection_receipt(places,counties)
    return {"place_count":len(places),"county_count":len(counties),"edges":edges}

def sets(edges):
    result=defaultdict(set)
    for e in edges:
        p,c=e["place_geoid"],e["county_geoid"]
        if len(p)!=7 or len(c)!=5 or not p.startswith("55") or not c.startswith("55"):
            raise ValueError("STATE_EDGE_INVALID")
        if c in result[p]:
            raise ValueError("DUPLICATE_EDGE")
        result[p].add(c)
    return result

def diff(old,new):
    before,after=sets(old),sets(new)
    changes=[]
    labels=["UNCHANGED_COUNTY_SET","COUNTY_SET_CHANGED","NEW_IN_2026_EXTRACT","ABSENT_FROM_2026_EXTRACT"]
    counts=dict.fromkeys(labels,0)
    for geoid in sorted(set(before)|set(after)):
        b=before.get(geoid,set());a=after.get(geoid,set())
        label=("NEW_IN_2026_EXTRACT" if geoid not in before else
               "ABSENT_FROM_2026_EXTRACT" if geoid not in after else
               "UNCHANGED_COUNTY_SET" if a==b else "COUNTY_SET_CHANGED")
        counts[label]+=1
        if label!="UNCHANGED_COUNTY_SET":
            changes.append({"place_geoid":geoid,"classification":label,
                "before_counties":sorted(b),"after_counties":sorted(a),
                "added":sorted(a-b),"removed":sorted(b-a),
                "bas_causation":"HOLD"})
    return counts,changes

def bas_candidate_rows(raw,src,targets):
    data=raw.decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(data,newline=""),delimiter="\t")
    if tuple(reader.fieldnames or ())!=BAS_HEADER:
        raise ValueError("BAS_SCHEMA_DRIFT")
    matched=[];total=0
    for row in reader:
        total+=1
        if None in row or row["State FIPS"]!="55" or row["State USPS"]!="WI":
            raise ValueError("BAS_ROW_INVALID")
        if row["GEOID"] in targets:
            if row["Entity FIPS Code"]!=row["GEOID"][2:]:
                raise ValueError("BAS_ID_CONFLICT")
            matched.append({"place_geoid":row["GEOID"],"year":src["year"],
               "county_geoid":"55"+row["County FIPS Code"],
               "bas_id":row["BAS ID"],"gcatoid":row["GCATOID"],
               "action":row["Action"],"effective_number":row["Local Effective Number"] or None,
               "effective_date":row["Local Effective Date"] or None,
               "source_sha256":src["sha256"],"status":"SAME_GEOID_CANDIDATE_CAUSATION_HOLD"})
    return total,matched

def run(fetcher=download):
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    src=manifest["sources"]
    if manifest["schema"]!="cw-wi-census-2020-2026-bas-source-pins-v0.1" or manifest["state_fips"]!="55" or len(src)!=8:
        raise ValueError("MANIFEST_INVALID")
    indexed={s["kind"]:s for s in src if s["kind"]!="bas"}
    bas=[s for s in src if s["kind"]=="bas"]
    if set(indexed)!=EXPECTED_KINDS or [s["year"] for s in bas]!=list(range(2021,2026)):
        raise ValueError("SOURCE_SET_INCOMPLETE")
    raw={k:verify_bytes(fetcher(s),s) for k,s in indexed.items()}
    baseline=import_bytes(raw["2020_place_by_county"],source_url=indexed["2020_place_by_county"]["url"],
       vintage="2020",expected_sha256=indexed["2020_place_by_county"]["sha256"],expected_state=STATE)
    current=build_spatial(raw["2026_places"],raw["2026_counties"])
    counts,changes=diff(baseline["edges"],current["edges"])
    changed_ids={x["place_geoid"] for x in changes}
    matches=[];bas_records={}
    for s in bas:
        n,rows=bas_candidate_rows(verify_bytes(fetcher(s),s),s,changed_ids)
        bas_records[str(s["year"])]=n
        matches.extend(rows)
    by_geoid=defaultdict(list)
    for row in matches:
        by_geoid[row["place_geoid"]].append(row)
    for change in changes:
        change["bas_candidates"]=sorted(by_geoid[change["place_geoid"]],key=lambda x:(x["year"],x["gcatoid"]))
    return {"schema":"cw-wi-2020-2026-geographic-delta-bas-candidates-v0.1",
      "state_fips":"55","sources":[{"kind":s["kind"],"year":s.get("year"),
         "url":s["url"],"sha256":s["sha256"],"bytes":s["bytes"]} for s in src],
      "historical_edge_count":baseline["edge_count"],
      "current_place_count":current["place_count"],
      "current_county_count":current["county_count"],
      "current_edge_count":len(current["edges"]),
      "historical_multicounty_count":baseline["multicounty_place_count"],
      "current_multicounty_count":sum(len(x)>1 for x in sets(current["edges"]).values()),
      "delta_counts":counts,"changes":changes,
      "bas_row_counts":bas_records,"bas_candidate_count":len(matches),
      "causation_established":False,"legal_authority":False,"wallet_signed":False,
      "status":"2020_TO_2026_GEOGRAPHY_OBSERVED_BAS_CAUSATION_HOLD"}

if __name__=="__main__":
    out=run()
    data=(json.dumps(out,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
    target=Path("wi-2020-2026-delta-bas-candidates.json")
    if target.exists():
        raise SystemExit("OUTPUT_EXISTS_FAIL_CLOSED")
    target.write_bytes(data)
    print("CW_WI_DELTA_PASS counts=%s edges=%d multicounty=%d bas_candidates=%d sha256=%s"%
       (json.dumps(out["delta_counts"],sort_keys=True,separators=(",",":")),
       out["current_edge_count"],out["current_multicounty_count"],
       out["bas_candidate_count"],hashlib.sha256(data).hexdigest()))
    print("CW_WI_CHANGED_PLACE_GEOIDS="+json.dumps([{"geoid":v["place_geoid"],"class":v["classification"],"bas_count":len(v["bas_candidates"])} for v in out["changes"]],separators=(",",":")))
