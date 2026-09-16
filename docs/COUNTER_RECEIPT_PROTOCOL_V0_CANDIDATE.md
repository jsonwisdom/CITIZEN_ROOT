# COUNTER_RECEIPT_PROTOCOL_V0

STATUS: SEATED_AS_CANDIDATE / EXTERNALIZED
CHAIN_POSITION: O3½ (predicate membrane) → O4
AUTHORITY_GRANTED: FALSE
DRIFT: NONE
ROLE: Defines the sole mechanism by which a counter_receipt may be issued, referenced, or resolved against any promotion packet or target-acceptance evaluation.

Referenced by:

- `counter_receipt_refs`
- `PKT_COUNTER_RECEIPTS_NONE`

## Continuity note

An earlier `COUNTER_RECEIPT_PROTOCOL_V0` definition remains embedded in `APPLE_BLOSSOM_QUAD_ONION_LOCKSET_V0`. This standalone file externalizes the later O3½ candidate declaration without rewriting those older bytes. Promotion over the embedded definition requires an explicit version-resolution artifact; this file does not silently overwrite history.

## Root invariant

```text
EACH_LAYER FEEDS THE NEXT
NONE PROVE THE NEXT
```

A counter-receipt is pure negative evidence.
It never grants authority.
It never promotes.
It never collapses layers.
It only forces HOLD or REJECT_INVALID.

## Counter-receipt universe

Closed, enumerated, non-extensible without a new artifact.

```text
counter_receipt_id := ENUM {
  CR_SHAPE_INVALID,
  CR_SCHEMA_VERSION_UNACCEPTABLE,
  CR_CANONICALIZATION_BROKEN,
  CR_HASH_CHAIN_BROKEN,
  CR_SOURCE_RUNG_UNDECLARED,
  CR_SOURCE_RUNG_INELIGIBLE,
  CR_SOURCE_RUNG_SELF_PROMOTING,
  CR_SOURCE_RUNG_CIRCULAR,
  CR_SOURCE_RUNG_RECURSIVE,
  CR_AUTHORITY_REFS_IMPLY_GRANT,
  CR_TARGET_RULESET_UNBOUND,
  CR_TARGET_RULESET_VERSION_UNACCEPTABLE,
  CR_TARGET_RULESET_DEPRECATED,
  CR_TARGET_RULESET_NON_CANONICAL,
  CR_REPLAY_TRACE_HASH_INVALID,
  CR_REPLAY_TRACE_NON_RECONSTRUCTIBLE,
  CR_REPLAY_TRACE_DIVERGENT,
  CR_REPLAY_TRACE_STALE,
  CR_EVIDENCE_LOCATORS_ABSENT,
  CR_EVIDENCE_LOCATORS_FAULTY,
  CR_EVIDENCE_LOCATORS_MISSING,
  CR_EVIDENCE_CANONICALIZATION_BROKEN,
  CR_EVIDENCE_HASH_CHAIN_BROKEN,
  CR_AUTHORITY_IMPERSONATION,
  CR_LAYER_IMPERSONATION,
  CR_RUNG_IMPERSONATION,
  CR_RECEIPT_IMPERSONATION,
  CR_BOUNDARY_COLLAPSE,
  CR_PARENT_DRIFT,
  CR_CHILD_DRIFT,
  CR_GRAMMAR_DRIFT,
  CR_CANON_DRIFT
}
```

## Counter-receipt semantics

Each `counter_receipt_id` is a semantic atom. No implication, upward collapse, or authority creation is permitted.

A counter-receipt is issued only when a corresponding predicate evaluates FALSE or remains unresolved under additional examination.

Issuance rules:

- MUST reference the exact promotion packet hash under challenge.
- MUST declare the exact failed or unresolved `predicate_id`.
- MUST carry its own independent hash chain.
- MUST never claim authority, admission, or truth.
- MUST never attempt self-promotion or circular reference.

Resolution rules:

- Presence of any counter-receipt forces the three-list evaluation into HOLD or REJECT_INVALID.
- Only explicit, later, independent clearance of every referenced `counter_receipt_id` can restore a path to ACCEPT_AS_INPUT.
- Clearance itself is a new receipt; it never retroactively grants authority.

## Integration with target acceptance

Within `TARGET_ACCEPTANCE_RECEIPT_SCHEMA_V0`:

- Any non-empty `counter_receipt_refs` → `PKT_COUNTER_RECEIPTS_NONE` evaluates FALSE.
- All listed `counter_receipt_id` values MUST be examined.
- Unresolved counter-receipts remain in `unresolved_predicates`.
- Failed counter-receipts remain in `failed_predicates`.

```text
COUNTER_RECEIPT != POSITIVE_EVIDENCE
COUNTER_RECEIPT != AUTHORITY
COUNTER_RECEIPT != PROMOTION
```

No counter-receipt crosses an onion boundary.

## Seal

```text
ROOT_INVARIANT_CHARTER_V0
→ DEVELOPMENTAL_GRAMMAR_V0
→ APPLE_BLOSSOM_QUAD_ONION_V0
→ SEED_TO_INSTITUTION_LADDER_V0
→ PROMOTION_PACKET_SCHEMA_V0
→ TARGET_ACCEPTANCE_RECEIPT_SCHEMA_V0
→ RUNG_GATE_PREDICATES_V0
→ COUNTER_RECEIPT_PROTOCOL_V0
```

AUTHORITY_GRANTED_BY_THIS_ARTIFACT: FALSE
