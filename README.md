# CITIZEN_ROOT

Thin federation root for verifiable civic infrastructure and Jay's public GitHub service.

**Authority: false**

This repository holds pointers, digests, verification rules, and discovery surfaces. Actual evidence and protocol artifacts remain in their source repositories and protected storage surfaces.

## Jay's GitHub as a Service for the Public

Start here:

- `docs/JAYS_GITHUB_AS_A_SERVICE_V0_1.md` — public service contract and visibility membrane
- `registry/REPOSITORY_SERVICE_INDEX_V0_1.json` — machine-readable public repository inventory
- `CITIZEN_ROOT_INDEX.json` — root pointer registry

Current inventory boundary:

```text
TOTAL_GITHUB_REPOSITORIES = 87
PUBLIC_REPOSITORIES       = 80
PRIVATE_REPOSITORIES      = 7
SECRET_VALUES_INDEXED     = 0
AUTHORITY_CREATED         = FALSE
```

Public repositories are discoverable. Private repository names and protected Drive pointers stay in the private control plane. Family routing is pointer-only and does not create identity, consent, custody, ownership, school status, or authority. Secret values never belong in this Git history.

## Core source surfaces

- AL — protocol / agent / receipt foundation
- JOY — integration / replay / family routing receipts
- COMPUTERWISDOM — evidence / historical archive
- HEIDEE — focused public surface

## Invariants

1. No evidence is duplicated here merely to make the index convenient. Prefer pointers, receipts, immutable hashes, and source anchors.
2. Translations and jurisdiction packs are derived leaves that reference `source_sha256`. They cannot replace the source.
3. Claim status is append-only. Original claim leaves are never deleted.
4. The root index itself is data, not authority. Anyone can mirror it and still verify the chain.
5. `MISSING_RECEIPT -> HOLD`.
6. `SEARCH_MISS != NO_WORK`.
7. `REPO != PERSON`.
8. `SECRET_POINTER != SECRET_VALUE`.

## Current state (v0.1.0)

Public service index populated. Root hash / Merkle freeze is still pending.

Sequence for a future freeze:

1. Canonicalize `CITIZEN_ROOT_INDEX.json` and registered leaves.
2. SHA-256 each canonical leaf.
3. Populate the root receipt.
4. Construct the ordered Merkle set.
5. Publish the verified root state.

## Layout

```text
CITIZEN_ROOT/
├── CITIZEN_ROOT_INDEX.json
├── docs/
│   └── JAYS_GITHUB_AS_A_SERVICE_V0_1.md
├── registry/
│   └── REPOSITORY_SERVICE_INDEX_V0_1.json
├── receipts/
│   └── CITIZEN_ROOT_INDEX_ROOT_RECEIPT_V0_1.json
├── agent_discovery/
├── claim_status/
├── jurisdictions/
├── languages/
├── verification/
└── mirrors/
```
