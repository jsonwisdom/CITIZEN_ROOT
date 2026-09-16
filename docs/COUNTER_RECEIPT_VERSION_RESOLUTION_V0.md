# COUNTER_RECEIPT_VERSION_RESOLUTION_V0

NAME: COUNTER_RECEIPT_VERSION_RESOLUTION_V0
PURPOSE: Bind old-definition ↔ later-candidate relationship without rewriting either artifact.
STATUS: SEATED / EXPLICIT_RESOLUTION
AUTHORITY_GRANTED: FALSE
PARENT: COUNTER_RECEIPT_VERSION_RESOLUTION declared 2026-09-16
UPSTREAM_OBJECTS:
  - APPLE_BLOSSOM_QUAD_ONION_LOCKSET_V0 (embedded ARTIFACT 5)
  - COUNTER_RECEIPT_PROTOCOL_V0_CANDIDATE.md (standalone O3½ file)

## Resolution type

This receipt resolves the *identity conflict*, not operational canonicity.

```text
CONFLICT_CLASS = SAME_SHORT_NAME_DISTINCT_BYTES
RESOLUTION_CLASS = BIND_AND_HOLD
SUPERSESSION = FALSE
DELETION = FALSE
REWRITE = FALSE
CANONICAL_VERSION = HOLD
```

A later file does not become the governor merely because it is later, searchable, or externalized.

## Bound identities

### A — EARLIER_EMBEDDED

```text
SHORT_NAME          = COUNTER_RECEIPT_PROTOCOL_V0
SURFACE             = EMBEDDED
CONTAINER           = docs/APPLE_BLOSSOM_QUAD_ONION_LOCKSET_V0.md
CONTAINER_BLOB      = 60b9b45aefc298af032e8fb2e3328c075678a078
SECTION             = ARTIFACT 5 — COUNTER_RECEIPT_PROTOCOL_V0
LAYER_DECLARED      = O3 — RECEIPT
SHAPE               = COUNTER_RECEIPT object + arrival protocol + resolution_receipt emit
CHALLENGE_TYPES     = EVIDENCE_MISMATCH | CLAIM_SCOPE | CLOCK_CONFLICT |
                      CHAIN_CONFLICT | BINDING_MISMATCH | REPLAY_FAILURE |
                      AUTHORITY_OVERREACH | OTHER
```

### B — LATER_CANDIDATE

```text
SHORT_NAME          = COUNTER_RECEIPT_PROTOCOL_V0
FILE_NAME           = COUNTER_RECEIPT_PROTOCOL_V0_CANDIDATE.md
SURFACE             = STANDALONE_FILE
PATH                = docs/COUNTER_RECEIPT_PROTOCOL_V0_CANDIDATE.md
COMMIT              = a7ef4197cdb8cf0dfb0c228c33c14e135b7bc495
BLOB                = 0d53743872692d40b1cd4ec3e44f30260903bf92
LAYER_DECLARED      = O3½ (predicate membrane) → O4
SHAPE               = closed counter_receipt_id enum + issuance/resolution rules
                      bound to promotion-packet / target-acceptance predicates
```

```text
A.SHORT_NAME = B.SHORT_NAME
A.BYTES     != B.BYTES
A.LAYER     != B.LAYER
A.SHAPE     != B.SHAPE
SAME_NAME   != SAME_OBJECT
```

## Relationship (non-superseding)

```text
B = EXTERNALIZED_CANDIDATE_OF_LATER_O3½_DECLARATION
A = PRIOR_EMBEDDED_O3_DEFINITION
B DOES_NOT_REWRITE A
B DOES_NOT_DELETE A
B DOES_NOT_AUTOMATICALLY_SUPERSEDE A
A DOES_NOT_BLOCK_OBSERVATION_OF B
```

Promotion of B over A requires a later, independent receipt whose `RESOLUTION_CLASS` is explicitly `SUPERSEDE` and which names both blob identities. This artifact is not that receipt.

## Core rules (locked)

1. `NEWER_DEFINITION != AUTOMATIC_SUPERSESSION`
2. `SAME_NAME != SAME_BYTES`
3. `SUPERSEDE REQUIRES EXPLICIT_RESOLUTION_RECEIPT` with `RESOLUTION_CLASS = SUPERSEDE`
4. Until such a supersession receipt exists:

```text
COUNTER_RECEIPT_CANONICAL_VERSION = HOLD
BOTH_VERSIONS = OBSERVED
BOTH_VERSIONS = NON_DELETED
BOTH_VERSIONS = NON_REWRITTEN
BOTH_VERSIONS = NON_CANONICAL
```

## Use while HOLD

Any packet, target-acceptance, or rung-gate evaluation that cites `COUNTER_RECEIPT_PROTOCOL_V0` MUST name which bound identity it uses:

```text
counter_receipt_protocol_ref := A | B | BOTH | UNDECLARED
UNDECLARED → HOLD
```

Citing the short name alone is insufficient.

## What this receipt does not do

```text
DOES_NOT_GRANT_AUTHORITY
DOES_NOT_PROMOTE_B
DOES_NOT_DEMOTE_A
DOES_NOT_MERGE_SHAPES
DOES_NOT_REWRITE_LOCKSET_BYTES
DOES_NOT_REWRITE_CANDIDATE_BYTES
DOES_NOT_CREATE_LEGAL_EFFECT
```

## Seal

```text
PERSISTENCE != PROMOTION
PROMOTION != AUTHORITY
SEARCH_MISS != TREE_ABSENCE
NEWER != CANON
NONE_PROVE_THE_NEXT
```

AUTHORITY_GRANTED_BY_THIS_ARTIFACT: FALSE
facts_promoted = 0
edges_inferred = 0
