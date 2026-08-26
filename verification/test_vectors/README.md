# test_vectors

Frozen cross-language vectors for the verification pipeline.

## Suites

| File | Focus |
|------|--------|
| `basic.json` | empty, already-canonical, simple structures |
| `whitespace.json` | CRLF, trailing spaces/tabs, BOM, pretty JSON |
| `unicode.json` | UTF-8, Markdown as opaque text |
| `nested.json` | key reorder, nested objects, escaped characters |

## Invariant

```
Python canonical bytes == Node canonical bytes
Python SHA-256         == Node SHA-256
```

Compare **bytes**, not only digests.

## Run

From `verification/`:

```bash
python3 selftest_canonicalize.py
node selftest_canonicalize.mjs
```

Machine-readable result (stdout):

```json
{
  "protocol": "CITIZEN_ROOT_INDEX_V0_1",
  "python_node_equivalence": true,
  "vectors_passed": 17,
  "vectors_failed": 0,
  "status": "PASS"
}
```

Fail closed: non-zero exit on any mismatch. No fallback canonicalizer.
