#!/usr/bin/env python3
"""CI-FIRST TIGER2026 Minnesota place x county polygon intersection replay.

Requires pyshp 2.3.1 and Shapely 2.1.2, installed by dedicated CI job.
Polygons use Census coordinates; positive area indicates geometric overlap,
NOT legal jurisdiction, dispatch authority, a change since 2020, or area in m².
"""
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "jurisdictions/MN_TIGER2026_PINNED_ZIP_SOURCE_MANIFEST.json"

def pinned_bytes(raw, source):
    if (len(raw) != source["bytes"] or
            hashlib.sha256(raw).hexdigest() != source["sha256"]):
        raise ValueError("SOURCE_ZIP_SHA256_OR_LENGTH_MISMATCH")
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("SOURCE_NOT_ZIP")
    return raw

def download(source):
    if source["url"] not in {
        "https://www2.census.gov/geo/tiger/TIGER2026/PLACE/tl_2026_27_place.zip",
        "https://www2.census.gov/geo/tiger/TIGER2026/COUNTY/tl_2026_us_county.zip"
    }:
        raise ValueError("SOURCE_URL_NOT_ALLOWLISTED")
    req = urllib.request.Request(source["url"], headers={
        "Accept-Encoding": "identity", "User-Agent": "CW-CI-FIRST/2026-geo"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        if (resp.status != 200 or resp.geturl() != source["url"] or
                resp.headers.get("Content-Encoding", "identity").lower() != "identity"):
            raise ValueError("SOURCE_HTTP_OR_REDIRECT_DRIFT")
        raw = resp.read(source["bytes"] + 1)
    return pinned_bytes(raw, source)

def shapefile_records(raw, kind):
    import shapefile
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if len(archive.infolist()) > 25:
            raise ValueError("ZIP_TOO_MANY_MEMBERS")
        members = {}
        for info in archive.infolist():
            if ("/" in info.filename or "\\" in info.filename or info.file_size > 400_000_000):
                raise ValueError("ZIP_MEMBER_UNSAFE")
            suffix = Path(info.filename).suffix.lower()
            if suffix in (".shp", ".shx", ".dbf"):
                if suffix in members:
                    raise ValueError("ZIP_DUPLICATE_COMPONENT")
                members[suffix] = archive.read(info)
        if set(members) != {".shp", ".shx", ".dbf"}:
            raise ValueError("MISSING_SHAPEFILE_COMPONENTS")
    reader = shapefile.Reader(shp=io.BytesIO(members[".shp"]),
                             shx=io.BytesIO(members[".shx"]),
                             dbf=io.BytesIO(members[".dbf"]))
    expected = {"place": {"STATEFP", "PLACEFP", "GEOID", "NAME"},
                "county": {"STATEFP", "COUNTYFP", "GEOID", "NAME"}}[kind]
    columns = [field[0] for field in reader.fields[1:]]
    if not expected.issubset(columns):
        raise ValueError("SHAPEFILE_SCHEMA_DRIFT")
    return reader

def intersection_receipt(place_features, county_features):
    from shapely.geometry import shape
    from shapely.strtree import STRtree
    import shapely
    county_geoms, county_codes = [], []
    for code, coordinates in county_features:
        poly = shape(coordinates)
        if not poly.is_valid or poly.is_empty or poly.area <= 0:
            raise ValueError("INVALID_COUNTY_GEOMETRY")
        county_codes.append(code)
        county_geoms.append(poly)
    if len(set(county_codes)) != len(county_codes):
        raise ValueError("DUPLICATE_COUNTIES")
    index = STRtree(county_geoms)
    edges = []
    seen_places = set()
    for place_code, coordinates in place_features:
        if place_code in seen_places:
            raise ValueError("DUPLICATE_PLACES")
        seen_places.add(place_code)
        place_poly = shape(coordinates)
        if not place_poly.is_valid or place_poly.is_empty or place_poly.area <= 0:
            raise ValueError("INVALID_PLACE_GEOMETRY")
        count = 0
        for idx in index.query(place_poly):
            county_poly = county_geoms[int(idx)]
            # Positive polygon intersection area, not mere border touch.
            if not place_poly.intersects(county_poly):
                continue
            overlap = place_poly.intersection(county_poly)
            if overlap.area <= 0:
                continue
            edges.append({"place_geoid": place_code,
                          "county_geoid": county_codes[int(idx)],
                          "relationship": "positive_polygon_area_overlap",
                          "source_vintage": 2026})
            count += 1
        if count == 0:
            raise ValueError("PLACE_WITHOUT_COUNTY_INTERSECTION:" + place_code)
    return sorted(edges, key=lambda x: (x["place_geoid"], x["county_geoid"]))

def run(sources=None):
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if (doc["schema"] != "cw-tiger-2026-mn-geometric-source-set-v0.1"
            or doc["vintage"] != 2026 or len(doc["sources"]) != 2
            or {s["kind"] for s in doc["sources"]} != {"place", "county"}
            or doc["authority"] is not False):
        raise ValueError("SOURCE_MANIFEST_NOT_ACCEPTABLE")
    blobs = {s["kind"]: pinned_bytes(sources[s["kind"]], s) if sources is not None
             else download(s) for s in doc["sources"]}
    places_reader = shapefile_records(blobs["place"], "place")
    county_reader = shapefile_records(blobs["county"], "county")
    places = []
    for rec in places_reader.iterShapeRecords():
        row = rec.record.as_dict()
        if row["STATEFP"] != "27" or row["GEOID"] != row["STATEFP"] + row["PLACEFP"]:
            raise ValueError("PLACE_IDENTIFIER_MISMATCH")
        places.append((row["GEOID"], rec.shape.__geo_interface__))
    counties = []
    for rec in county_reader.iterShapeRecords():
        row = rec.record.as_dict()
        if row["STATEFP"] == "27":
            if row["GEOID"] != row["STATEFP"] + row["COUNTYFP"]:
                raise ValueError("COUNTY_IDENTIFIER_MISMATCH")
            counties.append((row["GEOID"], rec.shape.__geo_interface__))
    edges = intersection_receipt(places, counties)
    minneapolis = sorted(x["county_geoid"] for x in edges if x["place_geoid"] == "2743000")
    if "27053" not in minneapolis:
        raise ValueError("MINNEAPOLIS_HENNEPIN_INTERSECTION_MISSING")
    multi = len({x["place_geoid"] for x in edges if sum(y["place_geoid"] == x["place_geoid"] for y in edges)>1})
    return {"schema":"cw-tiger2026-mn-place-county-spatial-overlap-v0.1",
            "sources":[{"kind":s["kind"],"url":s["url"],"bytes":s["bytes"],
                        "sha256":s["sha256"]} for s in doc["sources"]],
            "state":"27","vintage":2026,"places":len(places),"counties":len(counties),
            "edge_count":len(edges),"multicounty_place_count":multi,
            "minneapolis_counties":minneapolis,"edges":edges,
            "geography_verified":True,"legal_authority":False,
            "emergency_dispatch":False,"wallet_signed":False,
            "method":"positive_polygon_intersection_area_in_source_coordinates"}


if __name__ == "__main__":
    result = run()
    out = Path("mn-tiger2026-spatial-replay.json")
    if out.exists():
        raise SystemExit("OUTPUT_EXISTS_FAIL_CLOSED")
    encoded = (json.dumps(result,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
    out.write_bytes(encoded)
    print("CW_TIGER2026_MN_SPATIAL_PASS places=%d counties=%d edges=%d multicounty=%d minneapolis=%s receipt_sha256=%s" %
          (result["places"],result["counties"],result["edge_count"],
           result["multicounty_place_count"],",".join(result["minneapolis_counties"]),
           hashlib.sha256(encoded).hexdigest()))
