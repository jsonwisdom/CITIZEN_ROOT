# test_vectors

Frozen cross-language vectors for canonicalization v0.1.0.

**Compatibility boundary.** These bytes are the protocol. The canonicalizers are not.

## Contract

Canonical **bytes** are the primary assertion. The digest is secondary.

```text
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

The suite fails if **one byte** differs — even if a later digest implementation still matches.

A digest tells us two byte strings match. The frozen canonical-byte expectation tells us what bytes the protocol actually requires.

## Layout

```text
test_vectors/
    VECTOR_MANIFEST_V0_1.json
    fixtures/<id>.input          # raw input bytes (git: -text)
    vectors/<id>.json            # frozen expectation
    run_canonicalization_cross.py
    run_canonicalization_py.py
    run_canonicalization_mjs.mjs
```

Each vector file:

```json
{
  "id": "json_nested_001",
  "input_file": "fixtures/json_nested_001.input",
  "format": "json",
  "expected_canonical_hex": "...",
  "expected_sha256": "..."
}
```

Hex keeps the expected canonical bytes unambiguous.

`VECTOR_MANIFEST_V0_1.json` records, for each vector:

- `vector_id`
- `input_sha256`
- `expected_canonical_sha256`
- `expected_canonical_length`

The vector suite is itself an independently verifiable artifact.

## Run

From `verification/`:

```bash
python3 test_vectors/run_canonicalization_cross.py
python3 test_vectors/run_canonicalization_py.py
node test_vectors/run_canonicalization_mjs.mjs
```

All three must exit 0. The cross runner is the freeze gate.

## Coverage

| Vector | What it locks |
| --- | --- |
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
| `text_already_canonical_001` | identity |
| `json_already_canonical_001` | identity |

Additional locked cases: UTF-8 BOM, bare CR, pretty JSON, empty object/array, JSON Unicode.

## Explicitly prohibited

- Editing `canonicalize.py` or `canonicalize.mjs` to make a vector pass
- Markdown structural rewrite
- Unicode NFC/NFD
- Whitespace changes inside prose (beyond trailing-ws strip)
- Regenerating expected hex because a digest implementation changed

`freeze_from_implementations.py` records what the locked implementations already produce. It is not a license to rewrite the protocol.

## Git

Fixture `.input` files are marked `-text` in `.gitattributes` so CRLF and BOM bytes are not rewritten.
