#!/usr/bin/env python3
"""Computer Wisdom: pinned U.S. Census place-by-county codes importer v0.1.

Source is a Census geographic codes *listing*, not a 2020-to-2010 relationship file.
Does not assert contemporary boundaries, legal authority, signed proofs, or emergency activation.
Stdlib-only; input can be caller-provided bytes or exact allowlisted HTTPS source.
"""
import argparse
import csv
import hashlib
import io
import json
import urllib.request
from collections import defaultdict

MN_2020_URL = "https://www2.census.gov/geo/docs/reference/codes2020/place_by_cou/st27_mn_place_by_county2020.txt"
MN_2020_SHA256 = "0dae02710c8ee1e39f426cb84c47a7eab25ca26c692f24784f89b20d3655e886"
FIELDS = ("STATE", "STATEFP", "COUNTYFP", "COUNTYNAME", "PLACEFP", "PLACENS",
          "PLACENAME", "TYPE", "CLASSFP", "FUNCSTAT")


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def import_bytes(raw, *, source_url, vintage, expected_sha256, expected_state="27"):
    if not isinstance(raw, bytes) or not raw or len(raw) > 10_000_000:
        raise ValueError("Source bytes missing or oversized")
    if len(expected_sha256) != 64 or hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("SOURCE_SHA256_MISMATCH")
    try:
        decoded = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("SOURCE_NOT_UTF8") from exc
    reader = csv.DictReader(io.StringIO(decoded, newline=""), delimiter="|")
    if tuple(reader.fieldnames or ()) != FIELDS:
        raise ValueError("SOURCE_COLUMNS_CHANGED")
    edges = {}
    places = defaultdict(set)
    lines = 0
    for row in reader:
        lines += 1
        if None in row or any(not isinstance(v, str) or not v for v in row.values()):
            raise ValueError("MALFORMED_SOURCE_RECORD")
        if (row["STATEFP"] != expected_state or
                len(row["STATEFP"]) != 2 or not row["STATEFP"].isdigit() or
                len(row["COUNTYFP"]) != 3 or not row["COUNTYFP"].isdigit() or
                len(row["PLACEFP"]) != 5 or not row["PLACEFP"].isdigit() or
                len(row["PLACENS"]) != 8 or not row["PLACENS"].isdigit()):
            raise ValueError("GEOGRAPHIC_IDENTIFIER_INVALID")
        place = row["STATEFP"] + row["PLACEFP"]
        county = row["STATEFP"] + row["COUNTYFP"]
        key = (place, county)
        if key in edges:
            raise ValueError("DUPLICATE_PLACE_COUNTY_EDGE")
        # Preserve Census type/class; incorporated places and CDPs are distinct.
        edges[key] = {"place_geoid": place, "county_geoid": county,
                      "place_name": row["PLACENAME"], "county_name": row["COUNTYNAME"],
                      "place_type": row["TYPE"], "classfp": row["CLASSFP"],
                      "funcstat": row["FUNCSTAT"], "placens": row["PLACENS"]}
        places[place].add(county)
    if not edges:
        raise ValueError("EMPTY_SOURCE")
    ordered = [edges[k] for k in sorted(edges)]
    result = {"schema": "cw-census-place-county-edges-v0.1",
              "source": {"url": source_url, "vintage": vintage,
                         "raw_sha256": expected_sha256, "raw_bytes": len(raw),
                         "record_count": lines,
                         "format": "Census 2020 geographic codes place_by_cou pipe-delimited"},
              "state_fips": expected_state,
              "edge_count": len(ordered),
              "multicounty_place_count": sum(len(c) > 1 for c in places.values()),
              "edges": ordered,
              "authority": False,
              "evidence_status": "HISTORICAL_GEOGRAPHY_ONLY",
              "wallet_signature": None}
    return result


def read_official_source(url=MN_2020_URL, timeout=20):
    if url != MN_2020_URL:
        raise ValueError("NETWORK_SOURCE_NOT_ALLOWLISTED")
    req = urllib.request.Request(url, headers={"Accept-Encoding": "identity",
                                               "User-Agent": "CW-CI-FIRST-Census/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        if response.status != 200 or response.headers.get("Content-Encoding", "identity").lower() != "identity":
            raise ValueError("SOURCE_HTTP_OR_ENCODING_INVALID")
        raw = response.read(10_000_001)
    return raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Exact locally preserved original input bytes")
    parser.add_argument("--fetch", action="store_true", help="Fetch allowlisted official Census URL")
    parser.add_argument("--out", help="Write derived JSON; never overwrites source")
    args = parser.parse_args()
    if bool(args.input) == bool(args.fetch):
        parser.error("Choose exactly one of --input or --fetch")
    raw = read_official_source() if args.fetch else open(args.input, "rb").read()
    result = import_bytes(raw, source_url=MN_2020_URL, vintage="2020",
                          expected_sha256=MN_2020_SHA256)
    output = canonical(result) + b"\n"
    if args.out:
        from pathlib import Path
        target = Path(args.out)
        if target.exists():
            raise SystemExit("OUTPUT_EXISTS_FAIL_CLOSED")
        target.write_bytes(output)
    else:
        print(json.dumps({"status": "PASS_HISTORICAL_CENSUS_ONLY",
                          "source_sha256": MN_2020_SHA256,
                          "edges": result["edge_count"],
                          "multicounty_places": result["multicounty_place_count"]},
                         sort_keys=True))


if __name__ == "__main__":
    main()
