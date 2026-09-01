# JAY_ONCHAIN_REPUTATION_LEDGER_V0 — Invariants

Status: FROZEN_V0  
Declared public subject reference: `jaywisdom.base.eth`  
Authority: false  
Identity equals legal person: false  
Wrongdoing inference: false  
Ledger type: continuity graph  
Live ingest: NOT_STARTED

## Purpose

This ledger records replayable continuity observations across public surfaces. It is not a ranking, verdict, legal-person proof, authority surface, or wrongdoing score.

## Frozen event classes

- `IDENTITY_EVENT`
- `BASE_ACTIVITY_EVENT`
- `ZORA_CREATION_EVENT`
- `ZORA_EXPORT_RECEIPT_EVENT`
- `GITHUB_HISTORY_EVENT`
- `CONFLICT_EVENT`

## Mandatory event envelope

Every event carries:

- `event_id`
- `event_class`
- `timestamp`
- `timestamp_precision`
- `surface`
- `subject_ref`
- `receipt_ref`
- `source_uri`
- `source_hash`
- `observed_value`
- `snapshot`
- `conflict_ref`
- `authority=false`
- `identity_equals_legal_person=false`
- `wrongdoing_inference=false`

No event may override the three constant-false fields.

## Core invariants

1. No edge without `receipt_ref`.
2. Conflicts are first-class events; a conflict does not imply wrongdoing.
3. `ZORA_EXPORT_RECEIPT_EVENT` requires `snapshot=true`; export counts never silently become live state.
4. Source-native time precedes ingest time for chronology. Ingest cannot rewrite historical ordering.
5. Continuity only; no scalar reputation. `universal_reputation_score` remains `null` in V0.
6. ENS, Basename, wallet, creator address, or GitHub references do not by themselves establish a legal person or officeholder.
7. Address roles are descriptive only.
8. GitHub may index a chain fact; the chain receipt remains the stronger source for the chain event.
9. Creation is not endorsement, sale, collector identity, or current market value.
10. Conflict is not wrongdoing.

## Descriptive address roles

Allowed values:

- `creator`
- `holder`
- `counterparty`
- `contract`
- `ens`
- `basename`
- `github`
- `portal`

`GOOD_ACTOR`, `BAD_ACTOR`, `TRUSTED`, and `UNTRUSTED` are rejected.

## Event semantics

### IDENTITY_EVENT

An authoritative or independently inspectable surface associated a public identifier with an address or another public identifier.

Does not mean wallet = legal person, wallet = officeholder, wallet = authority, or same display name = same controller.

### BASE_ACTIVITY_EVENT

A Base-chain state transition involving an indexed subject address was observed. `chain_id` is fixed to `8453`.

### ZORA_CREATION_EVENT

A Zora/Base receipt identifies a creator relationship to an on-chain object.

### ZORA_EXPORT_RECEIPT_EVENT

At a stated observation time, an exporter returned a stated collection of records. Export counts are historical snapshots only.

### GITHUB_HISTORY_EVENT

A GitHub commit, file, receipt, index, or directory provides a dated public continuity observation.

Allowed `observation_type` values: `IDENTITY_REFERENCE`, `CHAIN_RECEIPT`, `CREATOR_INDEX`, `DIRECTORY_ENTRY`, `EXPORT_RECEIPT`, `CONTINUITY_RECEIPT`.

### CONFLICT_EVENT

A replayable divergence exists between two event claims. Conflicts are never deleted merely because a later observation exists.

Conflict types: `ADDRESS_MISMATCH`, `TIMESTAMP_MISMATCH`, `COUNT_MISMATCH`, `IDENTIFIER_MISMATCH`, `CREATOR_MISMATCH`, `CHAIN_MISMATCH`, `SOURCE_DISAGREEMENT`.

Resolution states: `UNRESOLVED`, `RESOLVED_A`, `RESOLVED_B`, `BOTH_VALID_DIFFERENT_SCOPE`, `SUPERSEDED_BY_LATER_RECEIPT`.

## Deterministic chronology

For equal timestamps:

1. block height / log index
2. transaction index
3. source-native timestamp
4. GitHub commit timestamp
5. export timestamp
6. ingest timestamp
7. event ID lexical order

`ingest_timestamp` is metadata only and may not reorder an event when a source-native timestamp exists.

## Query posture

`Q1` through `Q7` remain `UNCOMPUTED` until explicit ingest authorization.

```text
EVENT != INTERPRETATION
OBSERVATION != REPUTATION SCORE
NAME != LEGAL PERSON
ACTIVITY != ENDORSEMENT
EXPORT != LIVE STATE
CONFLICT != WRONGDOING

AUTHORITY_CREATED   false
INGEST_STATUS       NOT_STARTED
LIVE_CHAIN_QUERY    false
Q1-Q7               UNCOMPUTED
```

Persistence of these bytes does not authorize live-chain ingest, computation, identity-to-legal-person binding, scoring, or authority creation.
