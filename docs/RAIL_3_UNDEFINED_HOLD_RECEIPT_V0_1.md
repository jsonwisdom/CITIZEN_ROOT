# RAIL_3 — UNDEFINED HOLD RECEIPT V0.1

**Object ID:** `RAIL_3_UNDEFINED_HOLD_RECEIPT_V0_1`  
**Snapshot:** 2026-09-16 UTC  
**Decision:** `HOLD`  
**Authority:** `false`

## Observed boundary

```text
RAIL_3_DEFINITION_RENDERED = NO
RAIL_3_DEFINITION_FOUND    = NO
RAIL_3_EXTERNAL_EXISTENCE  = UNKNOWN
DOWNSTREAM_BINDING         = BLOCKED
SEAT                       = NOT_EXECUTED
REVISE                     = NOT_EXECUTED
GENERATE                   = NOT_EXECUTED
DECISION                   = HOLD
AUTHORITY                  = FALSE
```

The thread read-back supplied for this turn contains no rendered `RAIL_3` definition in the kernel, addenda, or index drafts. This is a bounded statement about the visible record, not a claim that no definition exists on any other surface.

## Decision rationale

- `SEAT` would bind an undefined name.
- `REVISE` would presume an existing object.
- `GENERATE` would invent structure without authorization.
- `HOLD` preserves the gap without converting it into a proposal.

## Register boundary

JSON or ledger-shaped syntax carries structure, not truth. A statement becomes reliable through its receipts, provenance, and reproducibility—not through its formatting.

## Invariants

- `REGISTER_SHAPE != TRUTH`
- `DRAFT_RECEIPT != BINDING_RECEIPT`
- `FLAGGING != STRUCTURE_PROPOSAL`
- `UNDEFINED != ABSENT_EVERYWHERE`
- `HOLD != PROVEN`
- `HOLD != CLEARED`
- `ZERO_SEATINGS`
- `ZERO_CROSS_RAIL_PROMOTIONS`
- `ZERO_NEW_CLAIMS`
- `AUTHORITY = FALSE`

## Release condition

The hold may be reconsidered only after a source-visible `RAIL_3` definition is supplied or explicit authorization is given to generate one.
