# test_vectors

Frozen cross-language vectors for the verification pipeline.

Canonical bytes are the primary assertion. SHA-256 is secondary. Expected canonical bytes are stored as **hex** so the fixture is unambiguous and byte-level comparison is explicit.

Do not edit `../canonicalize.py` or `../canonicalize.mjs` to make a vector pass.

## Per-vector record

```json
{
  "id": "json_nested_001",
  "input_file": "fixtures/json_nested_001.input",
  "format": "json",
  "expected_canonical_hex": "...",
  "expected_sha256": "..."
}
```

Raw inputs live in `fixtures/<id>.input` (`*.input -text` in `.gitattributes`).

## Suites

Suite files are indexes of vector ids:

| File | Focus |
|------|--------|
| `basic.json` | empty, already-canonical, missing final newline, empty object/array |
| `whitespace.json` | CRLF, trailing spaces/tabs, mixed whitespace, BOM, CR-only, pretty JSON |
| `unicode.json` | UTF-8, Markdown as opaque text, JSON Unicode |
| `nested.json` | recursive key order, arrays preserved, escaped serialization |

## Coverage

| Vector | What it locks |
|--------|----------------|
| `text_crlf_001` | LF conversion |
| `text_trailing_spaces_001` | whitespace rule |
| `text_trailing_tabs_001` | whitespace rule |
| `text_missing_final_newline_001` | EOF behavior |
| `text_unicode_001` | UTF-8 |
| `json_nested_001` | recursive key ordering |
| `json_arrays_001` | array ordering preserved |
| `json_escaped_001` | serialization determinism |
| `text_empty_001` | zero-byte behavior |
| `text_markdown_001` | non-JSON preservation |
| `text_mixed_whitespace_001` | byte-level normalization |
| `text_already_canonical_001` / `json_already_canonical_001` | identity |
| `text_bom_001` | UTF-8 BOM stripped |
| `text_cr_only_001` | bare CR → LF |
| `json_pretty_001` | pretty-print collapse |
| `json_key_reorder_001` | top-level key sort |
| `json_empty_object_001` / `json_empty_array_001` | empty JSON containers |
| `json_unicode_001` | JSON Unicode serialization |

## Invariant

```
Python canonical bytes == Node canonical bytes == expected canonical bytes
Python SHA-256         == Node SHA-256         == expected SHA-256
```

Compare **bytes**, not only digests. Fail if one byte differs.

## Manifest

`VECTOR_MANIFEST_V0_1.json` records, for every vector:

- `vector_id`
- `input_sha256`
- `expected_canonical_sha256`
- `expected_canonical_length`

The vector suite is an independently verifiable artifact. Canonicalization v0.1.0 is the compatibility boundary.

## Run

From `verification/`:

```bash
python3 selftest_canonicalize.py
node selftest_canonicalize.mjs
python3 test_vectors/run_canonicalization_cross.py
```

Machine-readable result (stdout):

```json
{
  "protocol": "CITIZEN_ROOT_INDEX_V0_1",
  "python_node_equivalence": true,
  "vectors_passed": 20,
  "vectors_failed": 0,
  "status": "PASS"
}
```

Fail closed: non-zero exit on any mismatch. No fallback canonicalizer.
