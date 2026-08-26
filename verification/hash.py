#!/usr/bin/env python3
"""Thin SHA-256 helper. Leaf construction = SHA-256(canonical_bytes)."""
from __future__ import annotations
import hashlib
from typing import Union

def sha256(data: Union[bytes, bytearray, memoryview]) -> bytes:
    """Return 32-byte digest."""
    return hashlib.sha256(data).digest()

def sha256_hex(data: Union[bytes, bytearray, memoryview]) -> str:
    return hashlib.sha256(data).hexdigest()

if __name__ == "__main__":
    import sys
    raw = sys.stdin.buffer.read()
    print(sha256_hex(raw))
