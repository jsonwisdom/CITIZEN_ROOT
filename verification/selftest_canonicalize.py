#!/usr/bin/env python3
"""
CITIZEN_ROOT canonicalization self-test (Python).

Fail closed. Machine-readable result on stdout.
Proves Python results against frozen vectors, and when Node is available,
proves Python canonical bytes == Node canonical bytes for every vector.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from canonicalize import canonicalize, sha256_hex

PROTOCOL = "CITIZEN_ROOT_INDEX_V0_1"
VECTOR_DIR = Path(__file__).resolve().parent / "test_vectors"
VECTOR_FILES = ["basic.json", "whitespace.json", "unicode.json", "nested.json"]
NODE_EMIT = VECTOR_DIR / "emit_canonical_bytes.mjs"


def load_vectors():
    """Load suite indexes, then per-vector JSON + raw fixture bytes."""
    vectors = []
    for name in VECTOR_FILES:
        path = VECTOR_DIR / name
        if not path.exists():
            raise FileNotFoundError(f"missing vector suite: {path}")
        doc = json.loads(path.read_text(encoding="utf-8"))
        for vector_id in doc["vectors"]:
            record_path = VECTOR_DIR / "vectors" / f"{vector_id}.json"
            v = json.loads(record_path.read_text(encoding="utf-8"))
            v["_suite"] = name
            v["_raw"] = (VECTOR_DIR / v["input_file"]).read_bytes()
            v["_expected_bytes"] = bytes.fromhex(v["expected_canonical_hex"])
            vectors.append(v)
    return vectors


def run_python(v):
    force_json = True if v["format"] == "json" else False
    got = canonicalize(v["_raw"], path=None, force_json=force_json)
    return got, sha256_hex(got)


def run_node(v):
    """Invoke Node canonicalize for the same raw bytes; return (bytes, hex)."""
    node = shutil.which("node")
    if not node:
        return None
    force = "json" if v["format"] == "json" else "text"
    proc = subprocess.run(
        [node, str(NODE_EMIT), force],
        input=v["_raw"],
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"node failed for {v['id']}: {proc.stderr.decode('utf-8', errors='replace')}"
        )
    got = proc.stdout
    return got, sha256_hex(got)


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
        expected_bytes = v["_expected_bytes"]
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

        if got != expected_bytes:
            result["vectors_failed"] += 1
            result["failures"].append({
                "id": v["id"],
                "suite": v["_suite"],
                "error": "python canonical bytes mismatch (primary)",
                "expected_canonical_hex": expected_bytes.hex(),
                "got_canonical_hex": got.hex(),
            })
            continue
        if got_hash != expected_hash:
            result["vectors_failed"] += 1
            result["failures"].append({
                "id": v["id"],
                "suite": v["_suite"],
                "error": "python sha256 mismatch (secondary)",
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
