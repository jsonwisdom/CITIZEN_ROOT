#!/usr/bin/env python3
"""Cross-language freeze check.

For every vector:

    Python canonical bytes
            ==
    Node canonical bytes
            ==
    expected canonical bytes

    Python SHA-256
            ==
    Node SHA-256
            ==
    expected SHA-256

Fails if one byte differs — even if a later digest implementation still matches.
Also verifies VECTOR_MANIFEST_V0_1.json against the fixture files.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from canonicalize import canonicalize, sha256_hex  # type: ignore

VECTORS_DIR = Path(__file__).resolve().parent
MANIFEST = VECTORS_DIR / "VECTOR_MANIFEST_V0_1.json"
NODE_EMIT = VECTORS_DIR / "emit_canonical_bytes.mjs"


def node_canonicalize(raw: bytes, force_json: bool) -> bytes:
    proc = subprocess.run(
        ["node", str(NODE_EMIT), "json" if force_json else "text"],
        input=raw,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"Node canonicalizer failed: {proc.stderr.decode('utf-8', errors='replace')}"
        )
    return proc.stdout


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    vector_files = sorted((VECTORS_DIR / "vectors").glob("*.json"))
    failed = 0
    seen_ids: list[str] = []

    for path in vector_files:
        v = json.loads(path.read_text(encoding="utf-8"))
        vector_id = v["id"]
        seen_ids.append(vector_id)
        raw = (VECTORS_DIR / v["input_file"]).read_bytes()
        force_json = v["format"] == "json"
        expected = bytes.fromhex(v["expected_canonical_hex"])
        expected_hash = v["expected_sha256"]

        py_bytes = canonicalize(raw, path=None, force_json=force_json)
        node_bytes = node_canonicalize(raw, force_json=force_json)
        py_hash = sha256_hex(py_bytes)
        node_hash = sha256_hex(node_bytes)

        byte_ok = py_bytes == node_bytes == expected
        hash_ok = py_hash == node_hash == expected_hash
        if not byte_ok:
            print(f"FAIL bytes {vector_id}")
            print(f"  expected: {expected.hex()}")
            print(f"  python:   {py_bytes.hex()}")
            print(f"  node:     {node_bytes.hex()}")
            failed += 1
            continue
        if not hash_ok:
            print(f"FAIL hash  {vector_id}")
            print(f"  expected: {expected_hash}")
            print(f"  python:   {py_hash}")
            print(f"  node:     {node_hash}")
            failed += 1
            continue
        print(f"PASS {vector_id}")

    by_id = {item["vector_id"]: item for item in manifest["vectors"]}
    if sorted(by_id) != sorted(seen_ids):
        print("FAIL manifest vector set != vector JSON set")
        print(f"  manifest: {sorted(by_id)}")
        print(f"  files:    {sorted(seen_ids)}")
        failed += 1
    else:
        for vector_id in seen_ids:
            v = json.loads((VECTORS_DIR / "vectors" / f"{vector_id}.json").read_text())
            raw = (VECTORS_DIR / v["input_file"]).read_bytes()
            expected = bytes.fromhex(v["expected_canonical_hex"])
            entry = by_id[vector_id]
            checks = [
                (
                    "input_sha256",
                    entry["input_sha256"],
                    hashlib.sha256(raw).hexdigest(),
                ),
                (
                    "expected_canonical_sha256",
                    entry["expected_canonical_sha256"],
                    hashlib.sha256(expected).hexdigest(),
                ),
                (
                    "expected_canonical_sha256 vs vector digest",
                    entry["expected_canonical_sha256"],
                    v["expected_sha256"],
                ),
                (
                    "expected_canonical_length",
                    entry["expected_canonical_length"],
                    len(expected),
                ),
            ]
            for label, left, right in checks:
                if left != right:
                    print(f"FAIL manifest {vector_id} {label}: {left} != {right}")
                    failed += 1

    if failed:
        print(f"\n{failed} failure(s)")
        return 1
    print(f"\n{len(seen_ids)} vectors passed (Python == Node == expected bytes + SHA-256)")
    print("VECTOR_MANIFEST_V0_1.json verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
