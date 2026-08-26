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
    ├── basic.json
    ├── whitespace.json
    ├── unicode.json
    ├── nested.json
    └── README.md
```

## Canonicalization contract

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
```

Machine-readable result:

```json
{
  "protocol": "CITIZEN_ROOT_INDEX_V0_1",
  "python_node_equivalence": true,
  "vectors_passed": 17,
  "vectors_failed": 0,
  "status": "PASS"
}
```

Both implementations must report `python_node_equivalence: true` and `status: "PASS"`.

## Hash / Merkle

Thin SHA-256 helpers in `hash.py` / `hash.mjs`.
Ordered binary Merkle in `merkle.py` / `merkle.mjs`.

```bash
python3 merkle.py
node merkle.mjs
```

## Pipeline

```
canonicalization self-test
        ↓
Python canonical bytes == Node canonical bytes
        ↓
SHA-256
        ↓
Merkle
        ↓
inclusion proof
        ↓
four real repository leaves
```
