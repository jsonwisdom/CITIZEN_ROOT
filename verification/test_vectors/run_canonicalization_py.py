#!/usr/bin/env python3
"""Run frozen vectors against canonicalize.py.

Primary assertion: canonical bytes == unhex(expected_canonical_hex).
Secondary assertion: SHA-256.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from canonicalize import canonicalize, sha256_hex  # type: ignore  # noqa: E402

VECTORS_DIR = Path(__file__).resolve().parent


def main() -> int:
    vector_files = sorted((VECTORS_DIR / "vectors").glob("*.json"))
    failed = 0
    for path in vector_files:
        v = json.loads(path.read_text(encoding="utf-8"))
        raw = (VECTORS_DIR / v["input_file"]).read_bytes()
        force_json = v["format"] == "json"
        expected = bytes.fromhex(v["expected_canonical_hex"])
        got = canonicalize(raw, path=None, force_json=force_json)
        got_hash = sha256_hex(got)
        if got != expected:
            print(f"FAIL bytes {v['id']}")
            print(f"  expected: {expected.hex()}")
            print(f"  got:      {got.hex()}")
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
    print(f"\n{len(vector_files)} vectors passed (Python bytes + SHA-256)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
