#!/usr/bin/env python3
"""Read-only nationwide Census 2020 place-to-county replay, SHA-256 pinned.

US 50 states + DC + AS, GU, MP, PR, VI: exactly 56 source files.
2020 geographic edges are historical, not 2026 legal or emergency authority.
No source files are changed, no wallets used, no private personal records.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request

from verification.import_census_place_county import import_bytes

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "jurisdictions/US_CENSUS_PLACE_BY_COUNTY_2020_SHA256_MANIFEST.json"
SOURCE_ROOT = "https://www2.census.gov/geo/docs/reference/codes2020/place_by_cou/"
FILE_PATTERN = re.compile(r"^st([0-9]{2})_([a-z]{2})_place_by_county2020\.txt$")
STATE_FIPS = frozenset("01 02 04 05 06 08 09 10 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56".split())
OTHER_FIPS = frozenset("11 60 66 69 72 78".split())
EXPECTED = STATE_FIPS | OTHER_FIPS


def load_manifest(path=MANIFEST_PATH):
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    if (manifest.get("schema") != "cw-census-place-by-county-national-source-set-v0.1"
            or manifest.get("source_root") != SOURCE_ROOT
            or manifest.get("vintage") != 2020
            or manifest.get("file_count") != 56):
        raise ValueError("UNTRUSTED_NATIONAL_MANIFEST_SCHEMA")
    sources = manifest.get("observations")
    if not isinstance(sources, list) or len(sources) != 56:
        raise ValueError("INCOMPLETE_NATIONAL_SOURCE_SET")
    seen = set()
    for src in sources:
        match = FILE_PATTERN.fullmatch(src.get("filename", ""))
        if not match:
            raise ValueError("UNTRUSTED_SOURCE_FILENAME")
        fips, abbrev = match.groups()
        if (src.get("state_fips") != fips or src.get("postal") != abbrev.upper()
                or fips in seen or fips not in EXPECTED):
            raise ValueError("SOURCE_STATE_OR_FILENAME_CONFLICT")
        seen.add(fips)
        if (not isinstance(src.get("bytes"), int) or src["bytes"] < 1
                or src["bytes"] > 10_000_000
                or not re.fullmatch("[0-9a-f]{64}", src.get("sha256", ""))):
            raise ValueError("INVALID_SOURCE_SIZE_OR_SHA256")
    if seen != EXPECTED:
        raise ValueError("COVERAGE_GAP")
    return sorted(sources, key=lambda s: s["state_fips"])


def download_source(src, timeout=30):
    # Only pinned, literal official Census host and exact manifest filename.
    url = SOURCE_ROOT + src["filename"]
    req = urllib.request.Request(url, headers={
        "Accept-Encoding": "identity", "User-Agent": "ComputerWisdom-CI-FIRST/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        final = urllib.parse.urlsplit(response.geturl())
        if (response.status != 200 or final.scheme != "https"
                or final.hostname != "www2.census.gov" or
                final.path != urllib.parse.urlsplit(url).path or
                response.headers.get("Content-Encoding", "identity").lower() != "identity"):
            raise ValueError("UNTRUSTED_RESPONSE_OR_REDIRECT")
        raw = response.read(10_000_001)
    if len(raw) != src["bytes"]:
        raise ValueError("SOURCE_SIZE_MISMATCH:" + src["state_fips"])
    if hashlib.sha256(raw).hexdigest() != src["sha256"]:
        raise ValueError("SOURCE_SHA256_MISMATCH:" + src["state_fips"])
    return raw


def replay_one(src, raw):
    if len(raw) != src["bytes"]:
        raise ValueError("SOURCE_BYTES_CHANGED:" + src["state_fips"])
    output = import_bytes(raw, source_url=SOURCE_ROOT + src["filename"],
                          vintage="2020", expected_sha256=src["sha256"],
                          expected_state=src["state_fips"])
    return {
        "state_fips": src["state_fips"],
        "source": src["filename"],
        "source_sha256": src["sha256"],
        "edge_count": output["edge_count"],
        "multicounty_place_count": output["multicounty_place_count"],
        "place_count": len({e["place_geoid"] for e in output["edges"]}),
        "county_count": len({e["county_geoid"] for e in output["edges"]}),
        "status": "PASS_2020_HISTORICAL_SOURCE_REPLAY",
    }


def replay_all(sources, downloader=download_source, max_workers=5):
    if len(sources) != 56 or {s["state_fips"] for s in sources} != EXPECTED:
        raise ValueError("COVERAGE_GAP")
    results = []
    # Exceptions from any future are not swallowed; fail closed, never partial PASS.
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        jobs = {pool.submit(downloader, src): src for src in sources}
        for future in as_completed(jobs):
            src = jobs[future]
            results.append(replay_one(src, future.result()))
    results.sort(key=lambda x: x["state_fips"])
    return {
        "schema": "cw-census-national-place-county-replay-v0.1",
        "source_vintage": 2020,
        "file_count": len(results),
        "state_count": len([r for r in results if r["state_fips"] in STATE_FIPS]),
        "additional_jurisdiction_count": len([r for r in results if r["state_fips"] in OTHER_FIPS]),
        "edges_total": sum(r["edge_count"] for r in results),
        "multicounty_places_total": sum(r["multicounty_place_count"] for r in results),
        "source_files": results,
        "legal_authority": False,
        "emergency_dispatch_authority": False,
        "wallet_signed": False,
        "national_2026_geography_verified": False,
        "disposition": "2020_HISTORICAL_ONLY_CURRENT_GEOGRAPHY_HOLD",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", default=str(MANIFEST_PATH))
    p.add_argument("--check-manifest", action="store_true")
    p.add_argument("--live", action="store_true")
    p.add_argument("--out", default=None)
    args = p.parse_args()
    sources = load_manifest(args.manifest)
    if args.check_manifest == args.live:
        p.error("Choose exactly one of --check-manifest and --live")
    if args.check_manifest:
        print(json.dumps({"status": "PASS_MANIFEST_STRUCTURE_ONLY",
                          "files": len(sources), "source_bytes_pinned": sum(x["bytes"] for x in sources)}))
        return
    result = replay_all(sources)
    encoded = (json.dumps(result, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False) + "\n").encode("utf-8")
    if args.out:
        path = Path(args.out)
        if path.exists():
            raise SystemExit("OUTPUT_EXISTS_FAIL_CLOSED")
        path.write_bytes(encoded)
    else:
        print(encoded.decode("utf-8"))
    print(f"CI_FIRST_2020_NATIONAL_PASS states={result['state_count']} extra={result['additional_jurisdiction_count']} edges={result['edges_total']} sha256={hashlib.sha256(encoded).hexdigest()}")


if __name__ == "__main__":
    main()
