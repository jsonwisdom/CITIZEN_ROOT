# test_vectors

Frozen cross-language vectors for the verification pipeline.

## Invariant

For every vector:

```
Python canonical bytes == Node canonical bytes
Python SHA-256         == Node SHA-256
```

Compare the **canonical bytes**, not only the digest. Matching digests with disagreeing serialization is a silent failure mode.

## Files

| File | Role |
|------|------|
| `canonicalization.json` | Frozen vectors (schema `CITIZEN_ROOT_CANONICALIZATION_VECTORS_V0_1`) |
| `run_canonicalization_py.py` | Python runner (byte equality) |
| `run_canonicalization_mjs.mjs` | Node runner (byte equality) |

## Run

From `verification/`:

```bash
python3 test_vectors/run_canonicalization_py.py
node test_vectors/run_canonicalization_mjs.mjs
```

Both must report every vector PASS and exit 0.

## Coverage

- CRLF → LF
- trailing spaces / tabs
- UTF-8 BOM
- Unicode (no NFC/NFD)
- empty files
- already-canonical input
- final newline behavior
- Markdown / plain text (opaque; no prose rewriting)
- nested JSON, arrays, escaped characters
- empty object / empty array

## Explicitly prohibited

- Markdown structural rewrite
- Unicode normalization (NFC/NFD)
- Whitespace changes inside prose (beyond trailing-ws strip)
- Line wrapping or reflow
- Any transformation not named in the locked protocol

The verifier determines identity. It does not decide what the artifact ought to say.
