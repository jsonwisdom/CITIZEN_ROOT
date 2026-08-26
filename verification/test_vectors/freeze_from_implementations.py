#!/usr/bin/env python3
"""Emit frozen vector files from the locked Python and Node canonicalizers.

Does not modify canonicalize.py / canonicalize.mjs.
Fails if Python and Node produce different canonical bytes for any fixture.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from canonicalize import canonicalize  # type: ignore  # noqa: E402

VECTORS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = VECTORS_DIR / "fixtures"
VECTOR_JSON_DIR = VECTORS_DIR / "vectors"
NODE_EMIT = VECTORS_DIR / "emit_canonical_bytes.mjs"

# Raw input bytes. These lock CRLF, tabs, BOM, and UTF-8 independently of JSON string escaping.
FIXTURE_SPECS: list[dict[str, object]] = [
    {
        "id": "text_crlf_001",
        "format": "text",
        "locks": "LF conversion",
        "input": b"hello\r\nworld\r\n",
    },
    {
        "id": "text_trailing_spaces_001",
        "format": "text",
        "locks": "whitespace rule (trailing spaces)",
        "input": b"hello  \nworld   \n",
    },
    {
        "id": "text_trailing_tabs_001",
        "format": "text",
        "locks": "whitespace rule (trailing tabs)",
        "input": b"a\tb\t\nc\t\t\n",
    },
    {
        "id": "text_missing_final_newline_001",
        "format": "text",
        "locks": "EOF behavior",
        "input": b"solo",
    },
    {
        "id": "text_unicode_001",
        "format": "text",
        "locks": "UTF-8 (no NFC/NFD)",
        "input": "café 日本語\n".encode("utf-8"),
    },
    {
        "id": "json_nested_001",
        "format": "json",
        "locks": "recursive key ordering",
        "input": b'{"z": {"b": 1, "a": 2}, "y": [3, 1]}\n',
    },
    {
        "id": "json_arrays_001",
        "format": "json",
        "locks": "array ordering preserved",
        "input": b'{"z":[3,1,2],"a":[1,2,3]}\n',
    },
    {
        "id": "json_escaped_001",
        "format": "json",
        "locks": "serialization determinism",
        "input": b'{"msg": "line\\nbreak\\tand\\"quote"}\n',
    },
    {
        "id": "text_empty_001",
        "format": "text",
        "locks": "zero-byte behavior",
        "input": b"",
    },
    {
        "id": "text_markdown_001",
        "format": "text",
        "locks": "non-JSON preservation",
        "input": (
            b"# Title\n\n- item one  \n- item two\n\nParagraph with  double spaces.\n"
        ),
    },
    {
        "id": "text_mixed_whitespace_001",
        "format": "text",
        "locks": "byte-level normalization",
        "input": b"  hello  \r\n\tworld \t\r\nkeep  middle\n",
    },
    {
        "id": "text_already_canonical_001",
        "format": "text",
        "locks": "identity",
        "input": b"line one\nline two\n",
    },
    {
        "id": "json_already_canonical_001",
        "format": "json",
        "locks": "identity",
        "input": b'{"a":1,"b":2}\n',
    },
    {
        "id": "text_bom_001",
        "format": "text",
        "locks": "UTF-8 BOM stripped",
        "input": b"\xef\xbb\xbfalpha\n",
    },
    {
        "id": "text_cr_only_001",
        "format": "text",
        "locks": "bare CR to LF",
        "input": b"one\rtwo\r",
    },
    {
        "id": "json_key_reorder_001",
        "format": "json",
        "locks": "object key sort + compact form",
        "input": b'{"b": 2, "a": 1}\n',
    },
    {
        "id": "json_pretty_001",
        "format": "json",
        "locks": "pretty JSON collapses to compact form",
        "input": b'{\n  "a": 1,\n  "b": 2\n}\n',
    },
    {
        "id": "json_empty_object_001",
        "format": "json",
        "locks": "empty object",
        "input": b"{}\n",
    },
    {
        "id": "json_empty_array_001",
        "format": "json",
        "locks": "empty array",
        "input": b"[]\n",
    },
    {
        "id": "json_unicode_001",
        "format": "json",
        "locks": "Unicode in JSON values (ensure_ascii=False)",
        "input": '{"name": "日本語"}\n'.encode("utf-8"),
    },
]


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
    if not NODE_EMIT.is_file():
        print(f"missing {NODE_EMIT}", file=sys.stderr)
        return 1

    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_JSON_DIR.mkdir(parents=True, exist_ok=True)

    manifest_vectors: list[dict[str, object]] = []
    mismatches: list[str] = []

    for spec in FIXTURE_SPECS:
        vector_id = str(spec["id"])
        fmt = str(spec["format"])
        raw = bytes(spec["input"])  # type: ignore[arg-type]
        force_json = fmt == "json"

        input_rel = f"fixtures/{vector_id}.input"
        input_path = VECTORS_DIR / input_rel
        input_path.write_bytes(raw)

        py_bytes = canonicalize(raw, path=None, force_json=force_json)
        node_bytes = node_canonicalize(raw, force_json=force_json)
        if py_bytes != node_bytes:
            mismatches.append(
                f"{vector_id}: Python {py_bytes.hex()} != Node {node_bytes.hex()}"
            )
            continue

        vector = {
            "id": vector_id,
            "input_file": input_rel,
            "format": fmt,
            "locks": spec["locks"],
            "expected_canonical_hex": py_bytes.hex(),
            "expected_sha256": sha256_hex(py_bytes),
        }
        (VECTOR_JSON_DIR / f"{vector_id}.json").write_text(
            json.dumps(vector, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        manifest_vectors.append(
            {
                "vector_id": vector_id,
                "input_sha256": sha256_hex(raw),
                "expected_canonical_sha256": sha256_hex(py_bytes),
                "expected_canonical_length": len(py_bytes),
            }
        )
        print(f"FROZEN {vector_id}  bytes={len(py_bytes)}  sha256={sha256_hex(py_bytes)}")

    if mismatches:
        print("\nPython/Node mismatch — freeze aborted:", file=sys.stderr)
        for line in mismatches:
            print(f"  {line}", file=sys.stderr)
        return 1

    manifest = {
        "schema_id": "CITIZEN_ROOT_VECTOR_MANIFEST_V0_1",
        "protocol_version": "0.1.0",
        "canonicalization": "UTF-8, LF, sorted object keys, no trailing whitespace",
        "hash_algorithm": "SHA-256",
        "authority": False,
        "principle": (
            "A digest tells us two byte strings match. "
            "The frozen canonical-byte expectation tells us what bytes the protocol actually requires."
        ),
        "compatibility_boundary": "canonicalization v0.1.0",
        "vectors": manifest_vectors,
    }
    (VECTORS_DIR / "VECTOR_MANIFEST_V0_1.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"\n{len(manifest_vectors)} vectors frozen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
