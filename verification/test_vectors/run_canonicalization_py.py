#!/usr/bin/env python3
"""Run frozen canonicalization vectors against canonicalize.py. Byte-level equality."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from canonicalize import canonicalize, sha256_hex  # type: ignore

VECTORS = Path(__file__).with_name("canonicalization.json")

def main() -> int:
    doc = json.loads(VECTORS.read_text(encoding="utf-8"))
    vectors = doc["vectors"]
    failed = 0
    for v in vectors:
        raw = v["input"].encode("utf-8")
        force_json = True if v["format"] == "json" else False
        got = canonicalize(raw, path=None, force_json=force_json)
        expected = v["expected_canonical"].encode("utf-8")
        got_hash = sha256_hex(got)
        if got != expected:
            print(f"FAIL bytes {v['id']}")
            print(f"  expected: {expected!r}")
            print(f"  got:      {got!r}")
            failed += 1
            continue
        if got_hash != v["expected_sha256"]:
            print(f"FAIL hash  {v['id']}: {got_hash} != {v['expected_sha256']}")
            failed += 1
            continue
        print(f"PASS {v['id']}")
    if failed:
        print(f"\n{failed} failure(s)")
        return 1
    print(f"\n{len(vectors)} vectors passed (Python)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
