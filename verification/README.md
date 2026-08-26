# verification

Canonicalization, hashing, Merkle construction, and replay helpers.

Rules (from CITIZEN_ROOT_INDEX):

- canonicalization: UTF-8, LF, sorted object keys, no trailing whitespace
- hash_algorithm: SHA-256
- leaf_construction: SHA-256(canonical_bytes)
- merkle_construction: ordered binary tree by path
- rewrite_forbidden: true
- authority: false
