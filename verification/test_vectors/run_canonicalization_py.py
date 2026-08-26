#!/usr/bin/env python3
"""Run frozen vectors against canonicalize.py.

Primary assertion: canonical bytes == unhex(expected_canonical_hex)
Secondary assertion: SHA-256(canonical bytes) == expected_sha256
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from canonicalize import canonicalize, sha256_hex  # type: ignore

VECTORS_DIR = Path(__file__).resolve().parent


def load_vectors() -> list[tuple[Path, dict]]:
    files = sorted((VECTORS_DIR / "vectors").glob("*.json"))
    return [(path, json.loads(path.read_text(encoding="utf-8"))) for path in files]


def main() -> int:
    failed = 0
    loaded = load_vectors()
    for path, v in loaded:
        vector_id = v["id"]
        raw = (VECTORS_DIR / v["input_file"]).read_bytes()
        force_json = True if v["format"] == "json" else False
        got = canonicalize(raw, path=None, force_json=force_json)
        expected = bytes.fromhex(v["expected_canonical_hex"])
        if got != expected:
            print(f"FAIL bytes {vector_id}")
            print(f"  expected_hex: {expected.hex()}")
            print(f"  got_hex:      {got.hex()}")
            failed += 1
            continue
        got_hash = sha256_hex(got)
        if got_hash != v["expected_sha256"]:
            print(f"FAIL hash  {vector_id}: {got_hash} != {v['expected_sha256']}")
            failed += 1
            continue
        print(f"PASS {vector_id}")
    if failed:
        print(f"\n{failed} failure(s)")
        return 1
    print(f"\n{len(loaded)} vectors passed (Python)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
