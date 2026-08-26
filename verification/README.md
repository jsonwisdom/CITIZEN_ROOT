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
├── hash.py
├── hash.mjs
├── merkle.py
├── merkle.mjs
└── test_vectors/
    ├── VECTOR_MANIFEST_V0_1.json
    ├── fixtures/<id>.input
    ├── vectors/<id>.json
    ├── run_canonicalization_cross.py
    ├── run_canonicalization_py.py
    ├── run_canonicalization_mjs.mjs
    └── README.md
```

## Canonicalization

Two equivalent, deterministic implementations of the locked specification.

| File | Language |
|------|----------|
| `canonicalize.py` | Python 3 |
| `canonicalize.mjs` | Node.js (ESM) |

Do not edit these files to make a vector pass. Canonicalization v0.1.0 is a compatibility boundary.

### Contract

```
raw artifact
   ↓
UTF-8 bytes
   ↓
LF line endings
   ↓
remove trailing whitespace
   ↓
parse structured formats where applicable (JSON only)
   ↓
sort object keys recursively
   ↓
emit canonical representation
   ↓
SHA-256(canonical_bytes)
```

Canonical **bytes** are the primary assertion. The digest is secondary.

```
Python canonical bytes
        ==
Node canonical bytes
        ==
expected canonical bytes
```

The suite fails if one byte differs — even if a later digest implementation still matches.

### Text rules

1. Decode as UTF-8 (strict). Strip BOM if present.
2. Normalize all line endings to LF (`\r\n` / `\r` → `\n`).
3. Strip trailing whitespace on every line.
4. Non-empty result ends with exactly one LF.
5. Empty input stays empty.

### JSON rules

1. Parse JSON.
2. Recursively sort object keys (array order preserved).
3. Serialize compact: `separators=(',', ':')`, `ensure_ascii=False`.
4. Single trailing LF. No trailing whitespace.

### Explicitly prohibited

- Markdown structural rewrite
- Unicode normalization (NFC/NFD)
- Whitespace changes inside prose (beyond trailing-ws strip)
- Line wrapping or reflow
- Any transformation not named in the locked protocol

The verifier determines identity. It does not decide what the artifact ought to say.

### Usage

```bash
python3 canonicalize.py                          # self-test
python3 canonicalize.py path/to/file.json
node canonicalize.mjs
node canonicalize.mjs path/to/file.md
```

Self-test sample (`{"b":2,"a":1}` → `{"a":1,"b":2}\n`):

```
e8d38819d39f705646bfb643368eca78f7db476c16471dbc33b941b27326410d
```

## Hash

Thin SHA-256 helpers. Leaf construction = SHA-256(canonical_bytes).

| File | Language |
|------|----------|
| `hash.py` | Python 3 |
| `hash.mjs` | Node.js (ESM) |

## Test vectors

Frozen cross-language vectors. Primary check is **byte equality** against `expected_canonical_hex`. SHA-256 is secondary. See `test_vectors/README.md`.

```bash
python3 test_vectors/run_canonicalization_cross.py
python3 test_vectors/run_canonicalization_py.py
node test_vectors/run_canonicalization_mjs.mjs
```

All three must report every vector PASS and exit 0. The cross runner is the freeze gate.

Coverage: CRLF→LF, trailing spaces/tabs, mixed whitespace, BOM, Unicode (no NFC/NFD), empty files, already-canonical input, final newline behavior, Markdown as opaque text, nested JSON, arrays, escaped characters.

## Merkle implementation

| File | Language |
|------|----------|
| `merkle.py` | Python 3 |
| `merkle.mjs` | Node.js (ESM) |

### Construction rules

1. Collect leaves as `{path, sha256}` where `sha256` is already the digest of the canonical bytes of the artifact.
2. Sort leaves strictly by `path` (lexicographic).
3. Build levels bottom-up by pairing consecutive hashes:
   - parent = SHA-256( left_raw_32_bytes + right_raw_32_bytes )
4. When a level has an odd number of nodes, the final unpaired node is **promoted** (not duplicated).
5. The single remaining hash is the Merkle root.

### Self-test

```bash
python3 merkle.py
node merkle.mjs
python3 canonicalize.py
node canonicalize.mjs
python3 test_vectors/run_canonicalization_cross.py
```

Self-tests must print deterministic output and "self-test passed". The vector suite must report every vector PASS.

## Pipeline

```
canonicalization tests
        ↓
Python canonical bytes == Node canonical bytes == expected bytes
        ↓
hash tests
        ↓
Merkle tests
        ↓
real repository leaves
        ↓
first mapped freeze
```

## Invariants

- Same ordered set of (path, sha256) pairs always produces the identical root.
- Inclusion proofs are compact and independently verifiable.
- Canonicalization is pure: same bytes in → same bytes out, across Python and Node.
- No central authority is required to recompute or check a proof.
