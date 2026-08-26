# verification

Canonicalization, hashing, Merkle construction, and replay helpers.

## Rules (from CITIZEN_ROOT_INDEX)

- **canonicalization**: UTF-8, LF, sorted object keys, no trailing whitespace
- **hash_algorithm**: SHA-256
- **leaf_construction**: SHA-256(canonical_bytes)
- **merkle_construction**: ordered binary tree by path
- **rewrite_forbidden**: true
- **authority**: false

## Layout

```
verification/
├── canonicalize.py
├── canonicalize.mjs
├── selftest_canonicalize.py
├── selftest_canonicalize.mjs
├── hash.py
├── hash.mjs
├── merkle.py
├── merkle.mjs
└── test_vectors/
    ├── VECTOR_MANIFEST_V0_1.json
    ├── fixtures/<id>.input
    ├── vectors/<id>.json
    ├── basic.json
    ├── whitespace.json
    ├── unicode.json
    ├── nested.json
    └── README.md
```

`canonicalize.py` and `canonicalize.mjs` are a **v0.1.0 compatibility boundary**. Do not edit them to make a vector pass. Change the protocol version instead.

## Canonicalization contract

A digest tells us two byte strings match. The frozen canonical-byte expectation tells us what bytes the protocol actually requires.

Primary assertion: canonical bytes. Secondary assertion: SHA-256.

### JSON

```
UTF-8
→ LF
→ remove trailing whitespace
→ recursively sort object keys
→ deterministic serialization
→ UTF-8 bytes
→ SHA-256
```

### Non-JSON

```
UTF-8
→ LF
→ remove trailing whitespace
→ otherwise preserve content exactly
→ SHA-256
```

### Explicitly prohibited

- Markdown structural rewrite
- Unicode normalization (NFC/NFD)
- Whitespace changes inside prose (beyond trailing-ws strip)
- Line wrapping or reflow
- Fallback canonicalizer on explicit JSON
- Locale-dependent sorting
- Platform-dependent newlines

Fail closed. The verifier determines identity; it does not decide what the artifact ought to say.

## Self-test

```bash
python3 selftest_canonicalize.py
node selftest_canonicalize.mjs
python3 test_vectors/run_canonicalization_cross.py
```

Machine-readable result:

```json
{
  "protocol": "CITIZEN_ROOT_INDEX_V0_1",
  "python_node_equivalence": true,
  "vectors_passed": 20,
  "vectors_failed": 0,
  "status": "PASS"
}
```

For every vector:

```
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
```

The test fails if one byte differs — even if a later digest implementation still matches.

## Hash / Merkle

Thin SHA-256 helpers in `hash.py` / `hash.mjs`.
Ordered binary Merkle in `merkle.py` / `merkle.mjs`.

```bash
python3 merkle.py
node merkle.mjs
```

## Pipeline

```
canonicalization self-test (frozen bytes + SHA-256)
        ↓
Python canonical bytes == Node canonical bytes == expected bytes
        ↓
SHA-256
        ↓
Merkle
        ↓
inclusion proof
        ↓
four real repository leaves (AL, JOY, COMPUTERWISDOM, HEIDEE)
```
