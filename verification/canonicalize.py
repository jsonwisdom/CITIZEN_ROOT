#!/usr/bin/env python3
"""
CITIZEN_ROOT canonicalization.

Rules (from CITIZEN_ROOT_INDEX verification_rules):
  canonicalization: UTF-8, LF, sorted object keys, no trailing whitespace
  hash_algorithm:   SHA-256
  leaf_construction: SHA-256(canonical_bytes)
  rewrite_forbidden: true
  authority: false

Deterministic. No randomness. No authority.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _strip_trailing_ws_lines(text: str) -> str:
    """Normalize each line: strip trailing whitespace, join with LF."""
    lines = text.split("\n")
    stripped = [line.rstrip(" \t\r\f\v") for line in lines]
    body = "\n".join(stripped)
    if body and not body.endswith("\n"):
        body += "\n"
    if body.endswith("\n\n"):
        body = body.rstrip("\n") + "\n"
    return body


def canonicalize_text(raw: Union[str, bytes]) -> bytes:
    """
    Text path:
      - UTF-8 decode (strict)
      - normalize all line endings to LF
      - strip trailing whitespace on every line
      - ensure non-empty result ends with exactly one LF
      - no BOM
    """
    if isinstance(raw, bytes):
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        text = raw.decode("utf-8")
    else:
        text = raw
        if text.startswith("\ufeff"):
            text = text[1:]

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _strip_trailing_ws_lines(text)
    return text.encode("utf-8")


def _sort_keys_recursive(obj: Any) -> Any:
    """Recursively sort object keys; leave arrays in order."""
    if isinstance(obj, dict):
        return {k: _sort_keys_recursive(obj[k]) for k in sorted(obj.keys())}
    if isinstance(obj, list):
        return [_sort_keys_recursive(v) for v in obj]
    return obj


def canonicalize_json(raw: Union[str, bytes, dict, list]) -> bytes:
    """
    JSON path:
      - parse (if needed)
      - recursively sort object keys
      - serialize compact: separators=(',', ':'), ensure_ascii=False
      - UTF-8, single trailing LF, no trailing whitespace
    """
    if isinstance(raw, (dict, list)):
        data = raw
    else:
        if isinstance(raw, bytes):
            if raw.startswith(b"\xef\xbb\xbf"):
                raw = raw[3:]
            text = raw.decode("utf-8")
        else:
            text = raw
            if text.startswith("\ufeff"):
                text = text[1:]
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        data = json.loads(text)

    ordered = _sort_keys_recursive(data)
    serialized = json.dumps(
        ordered,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    serialized = serialized.rstrip(" \t\r\n") + "\n"
    return serialized.encode("utf-8")


def detect_json(path: Optional[str], raw: bytes) -> bool:
    """Heuristic: .json extension or content starts with { or [ after whitespace."""
    if path and path.lower().endswith(".json"):
        return True
    sample = raw.lstrip()[:1]
    return sample in (b"{", b"[")


def canonicalize(
    raw: bytes,
    path: Optional[str] = None,
    force_json: Optional[bool] = None,
) -> bytes:
    """
    Apply the locked canonicalization rules.

    force_json:
      True  → always treat as JSON
      False → always treat as text
      None  → auto-detect
    """
    use_json = force_json if force_json is not None else detect_json(path, raw)
    if use_json:
        try:
            return canonicalize_json(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return canonicalize_text(raw)
    return canonicalize_text(raw)


def hash_canonical(
    raw: bytes,
    path: Optional[str] = None,
    force_json: Optional[bool] = None,
) -> Dict[str, Any]:
    """Return identity record for an artifact."""
    canonical = canonicalize(raw, path=path, force_json=force_json)
    digest = sha256_hex(canonical)
    return {
        "path": path,
        "sha256": digest,
        "size_bytes": len(canonical),
        "canonicalization": "UTF-8, LF, sorted object keys, no trailing whitespace",
        "hash_algorithm": "SHA-256",
    }


def canonicalize_file(filepath: str, force_json: Optional[bool] = None) -> Dict[str, Any]:
    """Read a file, canonicalize, return identity record + canonical bytes."""
    p = Path(filepath)
    raw = p.read_bytes()
    path_str = str(p).replace("\\", "/")
    record = hash_canonical(raw, path=path_str, force_json=force_json)
    record["canonical_bytes"] = canonicalize(raw, path=path_str, force_json=force_json)
    return record


def _self_test() -> None:
    failures = []

    raw_text = b"hello  \r\nworld\t\r\n"
    out = canonicalize_text(raw_text)
    expected = b"hello\nworld\n"
    if out != expected:
        failures.append(f"text CRLF: got {out!r} expected {expected!r}")

    bom = b"\xef\xbb\xbfalpha\n"
    out = canonicalize_text(bom)
    if out != b"alpha\n":
        failures.append(f"BOM: got {out!r}")

    j1 = b'{"b": 2, "a": 1}\n'
    j2 = b'{\n  "a": 1,\n  "b": 2\n}\n'
    c1 = canonicalize_json(j1)
    c2 = canonicalize_json(j2)
    if c1 != c2:
        failures.append(f"JSON order: {c1!r} != {c2!r}")
    if c1 != b'{"a":1,"b":2}\n':
        failures.append(f"JSON compact: got {c1!r}")

    nested = b'{"z": {"b": 1, "a": 2}, "y": [3, 1]}\n'
    cn = canonicalize_json(nested)
    if cn != b'{"y":[3,1],"z":{"a":2,"b":1}}\n':
        failures.append(f"nested JSON: got {cn!r}")

    d1 = sha256_hex(canonicalize(b'{"x":1,"y":2}'))
    d2 = sha256_hex(canonicalize(b'{"y":2,"x":1}'))
    if d1 != d2:
        failures.append("determinism failed")

    empty = canonicalize_text(b"")
    if empty != b"":
        failures.append(f"empty: got {empty!r}")

    if failures:
        for f in failures:
            print("FAIL:", f)
        sys.exit(1)

    print("canonicalize self-test passed")
    sample = canonicalize(b'{"b":2,"a":1}')
    print("sample_digest:", sha256_hex(sample))
    print("sample_bytes:", sample)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        _self_test()
    elif sys.argv[1] in ("-h", "--help"):
        print("Usage:")
        print("  python3 canonicalize.py              # self-test")
        print("  python3 canonicalize.py <file> [...] # print path + sha256")
        print("  python3 canonicalize.py --json <file>")
        print("  python3 canonicalize.py --text <file>")
        sys.exit(0)
    else:
        force = None
        args = sys.argv[1:]
        if args[0] == "--json":
            force = True
            args = args[1:]
        elif args[0] == "--text":
            force = False
            args = args[1:]
        for fp in args:
            rec = canonicalize_file(fp, force_json=force)
            print(json.dumps({
                "path": rec["path"],
                "sha256": rec["sha256"],
                "size_bytes": rec["size_bytes"],
            }, sort_keys=True))
