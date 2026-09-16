# PROMOTION_PACKET_SCHEMA_V0

PARENT: SEED_TO_INSTITUTION_LADDER_V0
STATUS: DEFINED / EXTERNALIZED
ROLE: CROSS-RUNG CANDIDATE TRANSPORT
AUTHORITY: NONE_GRANTED_BY_THIS_ARTIFACT

## Root invariant

```text
RUNG_n_OUTPUT
→ CANDIDATE_INPUT_FOR_RUNG_n+1

RUNG_n_OUTPUT
!= PROOF_OF_RUNG_n+1

TRANSPORT != ACCEPTANCE
ACCEPTANCE != VERIFICATION
VERIFICATION != AUTHORITY
```

## Byte-level shape

```text
PROMOTION_PACKET := {
  packet_id                 : UUID_v7 | deterministic_hash

  source := {
    rung                    : 0..5
    object_id               : stable_identifier
    version_id              : deterministic_hash
    content_digest          : hash(CANONICAL_CONTENT)
  }

  target := {
    rung                    : 0..5
    requested_evaluation    : opaque_identifier
  }

  provenance := {
    receipt_refs             : [receipt_id...]
    counter_receipt_refs     : [counter_receipt_id...]
    evidence_manifest        : locator | manifest_id | null
    canonicalization_version : identifier
    replay_procedure_hash    : deterministic_hash
  }

  unresolved_items          : [unresolved_item...]
  authority_refs            : [authority_reference...]
  emitted_at                : ISO8601_UTC
  emitter_id                : opaque_identifier
  prior_packet_id           : packet_id | null
  packet_digest             : hash(CANONICAL_PACKET_BODY)
}
```

## Required rules

1. `target.rung` MUST differ from `source.rung`.
2. Source object/version MUST remain immutable.
3. `unresolved_items` MUST survive transport unchanged unless resolved by a new receipt.
4. Missing authority references MUST remain empty.
5. No authority reference may be synthesized from title, relationship, scale, publication, possession, signature, or prior acceptance.
6. Counter-receipts MUST travel with the packet when applicable.
7. Evidence bytes not contained in the packet MUST have a resolvable manifest/locator for deterministic replay.
8. A changed packet creates a new `packet_id`; prior packet bytes remain intact.
9. Packet acceptance by the target rung MUST emit a separate target-rung receipt.

## Target-rung handling

```text
RECEIVE_PACKET
→ VALIDATE_PACKET_SHAPE
→ VALIDATE_SOURCE_IDENTITY
→ RESOLVE_RECEIPTS
→ RESOLVE_COUNTER_RECEIPTS
→ RESOLVE_EVIDENCE
→ REPLAY_SOURCE
→ PRESERVE_UNRESOLVED
→ APPLY_TARGET_RUNG_RULES
→ {ACCEPT_AS_INPUT | HOLD | REJECT_INVALID}
→ EMIT_TARGET_RECEIPT
```

## Failure-closed states

```text
MALFORMED_PACKET              → INVALID
SOURCE_DIGEST_MISMATCH        → FAILED
UNRESOLVED_REQUIRED_EVIDENCE  → HOLD
UNRESOLVED_COUNTER_RECEIPT    → HOLD
MISSING_REQUIRED_AUTHORITY    → HOLD
SOURCE_REPLAY_PASS            → ELIGIBLE_INPUT
```

```text
ELIGIBLE_INPUT != TARGET_PROVEN
```

The target rung MUST independently establish every predicate required by its own rules.

## Promotion membrane

```text
SOURCE_VERIFIED_RECEIPT
!= TARGET_VERIFIED_RECEIPT

SOURCE_AUTHORITY_REFERENCE
!= TARGET_AUTHORITY

PACKET_PRESENT
!= PACKET_ACCEPTED

PACKET_ACCEPTED
!= LEGAL_EFFECT
```

## Replay identity

```text
PACKET_IDENTITY :=
hash(
  schema_version
  || canonicalized_packet_body
)
```

Schema version and hash algorithm MUST be declared by the governing artifact.

## Seal

```text
PACKET_TRANSPORTS_RECEIPTS
PACKET_TRANSPORTS_UNRESOLVED_STATE
PACKET_TRANSPORTS_NO_AUTHORITY

NONE_PROVE_THE_NEXT
```

AUTHORITY_GRANTED_BY_THIS_ARTIFACT: FALSE
