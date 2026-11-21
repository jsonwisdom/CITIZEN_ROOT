#!/usr/bin/env python3
"""50-state aggregate root from exact original GitHub Actions receipt artifacts.

Strict immutable source-run binding and original CI-log SHA-256 checks. A
domain-separated Merkle root commits to state FIPS + JSON receipt SHA-256.
This establishes evidence integrity, NOT legal causation or government authority.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINS = ROOT / "jurisdictions/US_2026_STATE_RECEIPTS_ORIGINAL_LOG_SHA256_V0_1.json"
SOURCES = ROOT / "jurisdictions/US_TIGER2026_PLACE_SOURCE_PIN_COVERAGE_V0_1.json"
LEAF_PREFIX = b"cw-us26-leaf-v1\0"
NODE_PREFIX = b"cw-us26-node-v1\0"

def digest(data):
    return hashlib.sha256(data).digest()

def leaf(state, receipt_sha256):
    if len(state) != 2 or not state.isascii() or not state.isdigit():
        raise ValueError("INVALID_FIPS")
    if len(receipt_sha256) != 64 or any(c not in "0123456789abcdef" for c in receipt_sha256):
        raise ValueError("INVALID_RECEIPT_HASH")
    return digest(LEAF_PREFIX + state.encode("ascii") + bytes.fromhex(receipt_sha256))

def merkle_root(state_hashes):
    if not state_hashes:
        raise ValueError("EMPTY_ROOT")
    keys = sorted(state_hashes)
    if len(keys) != len(set(keys)):
        raise ValueError("DUPLICATE_STATE")
    row = [leaf(key, state_hashes[key]) for key in keys]
    while len(row) > 1:
        if len(row) % 2:
            row.append(row[-1])
        row = [digest(NODE_PREFIX + row[i] + row[i+1])
               for i in range(0, len(row), 2)]
    return row[0].hex()

def require_geoids(values, fips, width):
    if not isinstance(values, list) or values != sorted(set(values)):
        raise ValueError("UNSORTED_OR_DUPLICATE_GEOIDS")
    if any(not isinstance(s, str) or len(s) != width or
           not s.isascii() or not s.isdigit() or not s.startswith(fips)
           for s in values):
        raise ValueError("INVALID_STATE_GEOID")

def verify_state_receipt(raw, fips, pin, sources):
    if hashlib.sha256(raw).hexdigest() != pin:
        raise ValueError("ORIGINAL_LOG_RECEIPT_SHA256_MISMATCH:" + fips)
    try:
        rec = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("INVALID_RECEIPT_JSON:" + fips) from exc
    if ((json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8") != raw):
        raise ValueError("RECEIPT_NOT_CANONICAL:" + fips)
    if (rec.get("schema") != "cw-national-2026-state-build-receipt-v0.1"
        or rec.get("state_fips") != fips or rec.get("source_vintages") != [2020, 2026]
        or rec.get("status") != "GEOGRAPHY_CI_PASS_LEGAL_CAUSATION_HOLD"
        or rec.get("legal_causation_verified") is not False
        or rec.get("signed") is not False
        or rec.get("deployed") is not False):
        raise ValueError("RECEIPT_SCOPE_OR_GATES_INVALID:" + fips)
    expected_places = sources["pinned_states_by_fips"][fips]
    source_refs = rec.get("sources")
    if not isinstance(source_refs, list) or len(source_refs) != 3:
        raise ValueError("SOURCE_BINDING_MISSING:" + fips)
    by_role = {s.get("role"): s for s in source_refs}
    if len(by_role) != 3 or set(by_role) != {"historical", "places", "counties"}:
        raise ValueError("SOURCE_ROLES_INVALID:" + fips)
    for role, expected in [
        ("places", expected_places),
        ("counties", sources["county"]),
    ]:
        if by_role[role].get("url") != expected["url"] or by_role[role].get("sha256") != expected["sha256"]:
            raise ValueError("SOURCE_HASH_PIN_DRIFT:" + fips)
    historical = by_role["historical"]
    if (historical.get("url") !=
        "https://www2.census.gov/geo/docs/reference/codes2020/place_by_cou/" +
        sources["history_by_fips"][fips]["filename"]
        or historical.get("sha256") != sources["history_by_fips"][fips]["sha256"]):
        raise ValueError("HISTORICAL_SOURCE_MISMATCH:" + fips)
    for key in ("place_count", "county_count", "current_edges", "multicounty_places", "historical_edges"):
        n = rec.get(key)
        if type(n) is not int or n < 0:
            raise ValueError("NEGATIVE_OR_MISSING_METRIC:" + key)
    if (rec["place_count"] == 0 or rec["county_count"] == 0
        or rec["current_edges"] < rec["place_count"]
        or rec["multicounty_places"] > rec["place_count"]
        or rec["historical_edges"] == 0):
        raise ValueError("GEOGRAPHIC_COUNT_INVARIANT_FAIL:" + fips)
    labels = ("UNCHANGED_COUNTY_SET", "COUNTY_SET_CHANGED",
              "NEW_IN_2026_EXTRACT", "ABSENT_FROM_2026_EXTRACT")
    cnt = rec.get("delta_counts")
    if (not isinstance(cnt, dict) or set(cnt) != set(labels)
        or any(type(cnt[k]) is not int or cnt[k] < 0 for k in labels)):
        raise ValueError("DELTA_COUNTS_INVALID:" + fips)
    changes = rec.get("changed_places")
    if (not isinstance(changes, list) or len(changes) !=
        cnt["COUNTY_SET_CHANGED"] + cnt["NEW_IN_2026_EXTRACT"] +
        cnt["ABSENT_FROM_2026_EXTRACT"]):
        raise ValueError("DELTA_CHANGE_COUNT_MISMATCH:" + fips)
    geos = [x.get("place_geoid") for x in changes]
    require_geoids(geos, fips, 7)
    for x in changes:
        c = x.get("classification")
        if c not in labels[1:] or x.get("bas_legal_causation") != "HOLD":
            raise ValueError("DELTA_LEGAL_OR_CLASS_INVALID:" + fips)
        before, after = x.get("before_counties"), x.get("after_counties")
        require_geoids(before, fips, 5)
        require_geoids(after, fips, 5)
        if (x.get("added_counties") != sorted(set(after)-set(before))
            or x.get("removed_counties") != sorted(set(before)-set(after))):
            raise ValueError("DELTA_SET_DIFF_INVALID:" + fips)
        if (c == "COUNTY_SET_CHANGED" and (not before or not after or before == after)
            or c == "NEW_IN_2026_EXTRACT" and (before or not after)
            or c == "ABSENT_FROM_2026_EXTRACT" and (not before or after)):
            raise ValueError("DELTA_CATEGORY_INVALID:" + fips)
    if cnt["UNCHANGED_COUNTY_SET"] + len(changes) < rec["place_count"]:
        raise ValueError("PLACE_UNION_COUNT_FAIL:" + fips)
    return rec

def load_pins():
    p = json.loads(PINS.read_text(encoding="utf-8"))
    source = json.loads(SOURCES.read_text(encoding="utf-8"))
    historical = json.loads((ROOT / "jurisdictions/US_CENSUS_PLACE_BY_COUNTY_2020_SHA256_MANIFEST.json").read_text())
    states = p.get("states")
    state_pins = source.get("pinned_states")
    if (p.get("schema") != "cw-us-2026-state-receipt-original-log-pins-v0.1"
        or p.get("repository") != "jsonwisdom/CITIZEN_ROOT"
        or p.get("source_run_id") != 44873748371
        or p.get("source_commit") != "da992f4a902757409a29379794354b8d873d4559"
        or p.get("source_workflow_conclusion") != "success"
        or p.get("production_deployment") != "HOLD"
        or p.get("signing_authorized") is not False
        or source.get("coverage_state_count") != 50 or source.get("remaining_unpinned_states") != 0
        or source.get("not_nationwide_complete") is not False
        or not isinstance(states, dict) or len(states) != 50
        or not isinstance(state_pins, list) or len(state_pins) != 50
        or set(states) != {s["state_fips"] for s in state_pins}):
        raise ValueError("PIN_SET_INCOMPLETE_OR_UNTRUSTED")
    if not all(len(h) == 64 for h in states.values()):
        raise ValueError("BAD_HASH_PIN")
    return p, {"pinned_states_by_fips": {x["state_fips"]: x for x in state_pins},
               "county": source["county"],
               "history_by_fips": {x["state_fips"]: x for x in historical["observations"] if x["state_fips"] in states}}

def aggregate(directory):
    pins, sources = load_pins()
    paths = sorted(Path(directory).rglob("state-??-2026-geography.json"))
    if len(paths) != 50:
        raise ValueError("ARTIFACT_SET_NOT_50:" + str(len(paths)))
    got = {}
    state_rows = []
    totals = {"places": 0, "counties": 0, "place_county_edges": 0, "multicounty_places": 0,
              "historical_edges": 0, "changed_places": 0}
    for path in paths:
        fips = path.name[len("state-"):len("state-")+2]
        if fips in got or fips not in pins["states"] or path.is_symlink() or not path.is_file():
            raise ValueError("EXTRA_DUPLICATE_OR_UNTRUSTED_ARTIFACT:" + fips)
        rec = verify_state_receipt(path.read_bytes(), fips, pins["states"][fips], sources)
        got[fips] = pins["states"][fips]
        for output, key in [("places", "place_count"), ("counties", "county_count"),
                            ("place_county_edges", "current_edges"),
                            ("multicounty_places", "multicounty_places"),
                            ("historical_edges", "historical_edges")]:
            totals[output] += rec[key]
        totals["changed_places"] += len(rec["changed_places"])
        state_rows.append({"state_fips": fips, "receipt_sha256": got[fips],
                           "current_edges": rec["current_edges"],
                           "changed_places": len(rec["changed_places"])})
    if set(got) != set(pins["states"]):
        raise ValueError("MISSING_STATE_ARTIFACT")
    root = merkle_root(got)
    return {"schema": "cw-us-2026-national-50state-merkle-root-v0.1",
            "source_run_id": pins["source_run_id"],
            "source_commit": pins["source_commit"],
            "state_count": 50,
            "merkle_algorithm": "SHA256 domain-separated leaf fips+raw sha256; sorted ASCII FIPS; duplicate odd final node",
            "merkle_leaf_prefix": LEAF_PREFIX.hex(),
            "merkle_node_prefix": NODE_PREFIX.hex(),
            "national_merkle_root_sha256": root,
            "state_receipts": state_rows,
            "totals": totals,
            "source_integrity": "ALL_50_ORIGINAL_CI_LOG_HASHES_RECONFIRMED_FROM_ARTIFACT_BYTES",
            "legal_causation": "HOLD",
            "records_access_violations": "NONE_ESTABLISHED",
            "government_authority": False,
            "deployment": "HOLD",
            "wallet_signing": "HOLD"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", required=True)
    parser.add_argument("--output", default="cw-us-2026-national-merkle-root.json")
    args = parser.parse_args()
    result = aggregate(args.artifacts)
    data = (json.dumps(result, sort_keys=True, separators=(",", ":"))+"\n").encode()
    path = Path(args.output)
    if path.exists():
        raise SystemExit("OUTPUT_EXISTS_FAIL_CLOSED")
    path.write_bytes(data)
    print("CW_US_2026_NATIONAL_50_STATE_ROOT_PASS root=%s states=%d totals=%s receipt_sha256=%s" %
          (result["national_merkle_root_sha256"],result["state_count"],
           json.dumps(result["totals"],sort_keys=True,separators=(",", ":")),
           hashlib.sha256(data).hexdigest()))

if __name__ == "__main__":
    main()
