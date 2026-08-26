#!/usr/bin/env python3
"""
CITIZEN_ROOT canonicalization self-test (Python).

Fail closed. Machine-readable result on stdout.
Proves Python results against frozen vectors, and when Node is available,
proves Python canonical bytes == Node canonical bytes for every vector.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from canonicalize import canonicalize, sha256_hex

PROTOCOL = "CITIZEN_ROOT_INDEX_V0_1"
VECTOR_DIR = Path(__file__).resolve().parent / "test_vectors"
VECTOR_FILES = ["basic.json", "whitespace.json", "unicode.json", "nested.json"]


def load_vectors():
    vectors = []
    for name in VECTOR_FILES:
        path = VECTOR_DIR / name
        if not path.exists():
            raise FileNotFoundError(f"missing vector suite: {path}")
        doc = json.loads(path.read_text(encoding="utf-8"))
        for v in doc["vectors"]:
            v = dict(v)
            v["_suite"] = name
            vectors.append(v)
    return vectors


def run_python(v):
    raw = v["input"].encode("utf-8")
    force_json = True if v["format"] == "json" else False
    got = canonicalize(raw, path=None, force_json=force_json)
    return got, sha256_hex(got)


def run_node(v):
    """Invoke Node canonicalize for the same input; return (bytes, hex) or raise."""
    node = shutil.which("node")
    if not node:
        return None
    script = r"""
import { canonicalize } from './canonicalize.mjs';
import { createHash } from 'node:crypto';
const input = Buffer.from(process.argv[1], 'utf8');
const forceJson = process.argv[2] === 'json';
const got = canonicalize(input, null, forceJson);
const digest = createHash('sha256').update(got).digest('hex');
process.stdout.write(JSON.stringify({
  bytes_b64: got.toString('base64'),
  sha256: digest,
}));
"""
    force = "json" if v["format"] == "json" else "text"
    proc = subprocess.run(
        [node, "--input-type=module", "-e", script, v["input"], force],
        cwd=str(Path(__file__).resolve().parent),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"node failed for {v['id']}: {proc.stderr.strip()}")
    payload = json.loads(proc.stdout)
    import base64
    return base64.b64decode(payload["bytes_b64"]), payload["sha256"]


def main() -> int:
    result = {
        "protocol": PROTOCOL,
        "python_node_equivalence": None,
        "vectors_passed": 0,
        "vectors_failed": 0,
        "status": "FAIL",
        "failures": [],
        "suites": VECTOR_FILES,
    }

    try:
        vectors = load_vectors()
    except Exception as e:
        result["failures"].append({"id": "_load", "error": str(e)})
        result["vectors_failed"] = 1
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

    node_available = shutil.which("node") is not None
    equivalence_checked = 0
    equivalence_ok = True

    for v in vectors:
        expected_bytes = v["expected_canonical"].encode("utf-8")
        expected_hash = v["expected_sha256"]
        try:
            got, got_hash = run_python(v)
        except Exception as e:
            result["vectors_failed"] += 1
            result["failures"].append({
                "id": v["id"],
                "suite": v["_suite"],
                "error": f"python exception: {e}",
            })
            continue

        if got != expected_bytes or got_hash != expected_hash:
            result["vectors_failed"] += 1
            result["failures"].append({
                "id": v["id"],
                "suite": v["_suite"],
                "error": "python mismatch vs frozen vector",
                "expected_sha256": expected_hash,
                "got_sha256": got_hash,
            })
            continue

        if node_available:
            try:
                node_bytes, node_hash = run_node(v)
                equivalence_checked += 1
                if node_bytes != got or node_hash != got_hash:
                    equivalence_ok = False
                    result["vectors_failed"] += 1
                    result["failures"].append({
                        "id": v["id"],
                        "suite": v["_suite"],
                        "error": "python_node_bytes_mismatch",
                        "python_sha256": got_hash,
                        "node_sha256": node_hash,
                    })
                    continue
            except Exception as e:
                equivalence_ok = False
                result["vectors_failed"] += 1
                result["failures"].append({
                    "id": v["id"],
                    "suite": v["_suite"],
                    "error": f"node exception: {e}",
                })
                continue

        result["vectors_passed"] += 1

    if node_available:
        result["python_node_equivalence"] = (
            equivalence_ok and equivalence_checked == result["vectors_passed"]
            and result["vectors_failed"] == 0
        )
    else:
        result["python_node_equivalence"] = None

    result["status"] = "PASS" if result["vectors_failed"] == 0 else "FAIL"
    if result["vectors_failed"] > 0:
        result["status"] = "FAIL"

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
