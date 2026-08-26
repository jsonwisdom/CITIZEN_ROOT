# CITIZEN_ROOT

Thin federation root for verifiable civic infrastructure.

**Authority: false**

This repository holds only pointers, digests, verification rules, and discovery surfaces.
Actual evidence and protocol artifacts remain in:

- AL (protocol / agent / receipt foundation)
- JOY (integration / replay / archive)
- COMPUTERWISDOM (evidence / historical archive)
- HEIDEE (focused public surface)

## Invariants

1. No evidence is duplicated here. Only digests and pointers.
2. Translations and jurisdiction packs are derived leaves that reference `source_sha256`. They cannot replace the source.
3. Claim status is append-only. Original claim leaves are never deleted.
4. The root index itself is data, not authority. Anyone can mirror it and still verify the chain.

## Current state (v0.1.0)

Skeleton only. No artifacts populated. Root hash pending.

**Canonicalization v0.1.0 is a compatibility boundary.** Frozen vectors in `verification/test_vectors/` assert canonical **bytes** first and SHA-256 second, across Python and Node. Do not edit the canonicalizers to make a vector pass.

Sequence after the vector freeze:

1. First four real repository leaves: AL, JOY, COMPUTERWISDOM, HEIDEE
2. Write / finalize CITIZEN_ROOT_INDEX.json
3. Canonicalize
4. SHA-256 the root
5. Populate the root receipt
6. Canonicalize + hash the receipt
7. Construct Merkle set
8. Publish verified state

## Layout

```
CITIZEN_ROOT/
├── CITIZEN_ROOT_INDEX.json
├── receipts/
│   └── CITIZEN_ROOT_INDEX_ROOT_RECEIPT_V0_1.json
├── registry/
├── agent_discovery/
├── claim_status/
│   └── CLAIM_STATUS_CHANGE_LOG.jsonl
├── jurisdictions/
├── languages/
├── verification/
└── mirrors/
```
