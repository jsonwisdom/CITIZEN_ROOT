#!/usr/bin/env python3
"""
CITIZEN_ROOT ordered binary Merkle tree construction.

Rules (from CITIZEN_ROOT_INDEX verification_rules):
  - hash_algorithm: SHA-256
  - leaf_construction: SHA-256(canonical_bytes)
  - merkle_construction: ordered binary tree by path
  - rewrite_forbidden: true
  - authority: false

Deterministic. No randomness. No authority.
"""

from __future__ import annotations

import hashlib
import json
from typing import List, Dict, Any, Optional, Tuple


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_bytes(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def pair_hash(left_hex: str, right_hex: str) -> str:
    """Hash concatenation of two 32-byte digests (raw bytes, not hex strings)."""
    left = bytes.fromhex(left_hex)
    right = bytes.fromhex(right_hex)
    return sha256_hex(left + right)


def build_merkle_tree(leaves: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Build an ordered binary Merkle tree.

    Input leaves: list of {"path": str, "sha256": str}
    - Sorted strictly by path (lexicographic, UTF-8 code points).
    - Each leaf sha256 is already the SHA-256 of its canonical bytes.
    - Odd nodes are promoted (not duplicated).

    Returns:
      {
        "algorithm": "SHA-256",
        "construction": "ordered binary tree by path",
        "leaf_count": int,
        "root": str | null,
        "levels": list of lists of hex digests (level 0 = sorted leaves),
        "leaves": sorted list of {path, sha256}
      }
    """
    if not leaves:
        return {
            "algorithm": "SHA-256",
            "construction": "ordered binary tree by path",
            "leaf_count": 0,
            "root": None,
            "levels": [],
            "leaves": [],
        }

    # Strict sort by path
    sorted_leaves = sorted(leaves, key=lambda x: x["path"])

    # Level 0: the leaf hashes in path order
    current: List[str] = [leaf["sha256"] for leaf in sorted_leaves]
    levels: List[List[str]] = [current[:]]

    while len(current) > 1:
        next_level: List[str] = []
        i = 0
        while i < len(current):
            if i + 1 < len(current):
                parent = pair_hash(current[i], current[i + 1])
                next_level.append(parent)
                i += 2
            else:
                # Promote the unpaired node
                next_level.append(current[i])
                i += 1
        current = next_level
        levels.append(current[:])

    root = current[0] if current else None

    return {
        "algorithm": "SHA-256",
        "construction": "ordered binary tree by path",
        "leaf_count": len(sorted_leaves),
        "root": root,
        "levels": levels,
        "leaves": [{"path": l["path"], "sha256": l["sha256"]} for l in sorted_leaves],
    }


def verify_inclusion(
    leaf_path: str,
    leaf_sha256: str,
    proof: List[Dict[str, str]],
    root: str,
) -> bool:
    """
    Verify a Merkle inclusion proof.

    proof is a list of sibling steps from leaf toward root:
      [{"side": "left"|"right", "hash": "hex"}, ...]
    """
    current = leaf_sha256
    for step in proof:
        sibling = step["hash"]
        if step["side"] == "left":
            current = pair_hash(sibling, current)
        elif step["side"] == "right":
            current = pair_hash(current, sibling)
        else:
            return False
    return current == root


def generate_inclusion_proof(
    leaves: List[Dict[str, str]],
    target_path: str,
) -> Optional[Dict[str, Any]]:
    """
    Generate an inclusion proof for a given path.
    Returns None if the path is not present.
    """
    tree = build_merkle_tree(leaves)
    if tree["root"] is None:
        return None

    sorted_leaves = tree["leaves"]
    try:
        idx = next(i for i, l in enumerate(sorted_leaves) if l["path"] == target_path)
    except StopIteration:
        return None

    proof: List[Dict[str, str]] = []
    levels = tree["levels"]
    current_idx = idx

    for level in levels[:-1]:
        if current_idx % 2 == 0:
            # even index → sibling is right if it exists
            if current_idx + 1 < len(level):
                proof.append({"side": "right", "hash": level[current_idx + 1]})
            # else: promoted, no sibling
        else:
            # odd index → sibling is left
            proof.append({"side": "left", "hash": level[current_idx - 1]})
        current_idx //= 2

    return {
        "path": target_path,
        "leaf_sha256": sorted_leaves[idx]["sha256"],
        "proof": proof,
        "root": tree["root"],
    }


if __name__ == "__main__":
    # Minimal self-test
    sample = [
        {"path": "b.txt", "sha256": sha256_hex(b"content-b")},
        {"path": "a.txt", "sha256": sha256_hex(b"content-a")},
        {"path": "c.txt", "sha256": sha256_hex(b"content-c")},
    ]
    tree = build_merkle_tree(sample)
    print(json.dumps(tree, indent=2, sort_keys=True))

    proof = generate_inclusion_proof(sample, "a.txt")
    assert proof is not None
    assert verify_inclusion(
        proof["path"], proof["leaf_sha256"], proof["proof"], proof["root"]
    )
    print("self-test passed")
