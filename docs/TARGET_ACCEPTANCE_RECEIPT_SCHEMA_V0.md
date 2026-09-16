# TARGET_ACCEPTANCE_RECEIPT_SCHEMA_V0

PARENT: PROMOTION_PACKET_SCHEMA_V0
STATUS: DEFINED / EXTERNALIZED
ROLE: TARGET-RUNG INGEST / DISPOSITION RECEIPT
AUTHORITY: NONE_GRANTED_BY_THIS_ARTIFACT

## Root invariant

```text
PACKET_ACCEPTED != CLAIM_ACCEPTED
CLAIM_ACCEPTED != TARGET_VERIFIED
TARGET_VERIFIED != AUTHORITY

ACCEPT_AS_INPUT = PERMISSION_TO_EVALUATE
ACCEPT_AS_INPUT != TARGET_PROVEN
```

## Byte-level shape

```text
TARGET_RECEIPT := {
  target_receipt_id          : UUID_v7 | deterministic_hash
  promotion_packet_id        : packet_id
  promotion_packet_digest    : deterministic_hash
  target_rung                : 0..5
  target_ruleset_hash        : deterministic_hash
  target_ruleset_version     : identifier
  replay_trace_hash          : deterministic_hash

  source_replay_result       : ELIGIBLE_INPUT | HOLD | FAILED | INVALID
  target_disposition         : ACCEPT_AS_INPUT | HOLD | REJECT_INVALID

  satisfied_predicates       : [predicate_id...]
  unresolved_predicates      : [predicate_id...]
  failed_predicates          : [predicate_id...]

  authority_refs_examined    : [authority_reference...]
  counter_receipt_refs       : [counter_receipt_id...]

  emitted_at                 : ISO8601_UTC
  evaluator_id               : opaque_identifier
  prior_target_receipt_id    : target_receipt_id | null
  receipt_digest             : hash(CANONICAL_TARGET_RECEIPT_BODY)
}
```

## Validation rules

1. `promotion_packet_id` and `promotion_packet_digest` MUST resolve to the exact packet evaluated.
2. `target_rung` MUST equal the packet target rung.
3. `target_ruleset_hash` MUST bind the exact rules used for evaluation.
4. Every required predicate MUST appear in exactly one of the three predicate lists: satisfied, unresolved, or failed.
5. The three predicate lists MUST be mutually exclusive.
6. `authority_refs_examined` records references examined; presence does not imply authority.
7. Any non-empty `counter_receipt_refs` forces `PKT_COUNTER_RECEIPTS_NONE` to FALSE.
8. A changed evaluation emits a new target receipt; the prior receipt is not rewritten.

## Deterministic disposition

```text
STRUCTURAL_INVALIDITY
→ REJECT_INVALID

ANY_REQUIRED_PREDICATE_FAILED
→ REJECT_INVALID

NO_FAILED_PREDICATES
+ ANY_REQUIRED_PREDICATE_UNRESOLVED
→ HOLD

SOURCE_REPLAY_RESULT = ELIGIBLE_INPUT
+ ALL_REQUIRED_TARGET_GATE_PREDICATES_SATISFIED
+ PKT_COUNTER_RECEIPTS_NONE = TRUE
→ ACCEPT_AS_INPUT
```

`ACCEPT_AS_INPUT` means only that the packet may proceed to target-rung evaluation. It does not establish the target claim, authority, execution, receipt, or legal effect.

## Counter-receipt integration

```text
COUNTER_RECEIPT_PRESENT
→ PKT_COUNTER_RECEIPTS_NONE = FALSE
→ {HOLD | REJECT_INVALID}
```

Only a later, independent clearance receipt for every referenced counter-receipt may restore a path to `ACCEPT_AS_INPUT`.

```text
COUNTER_RECEIPT_CLEARED != TARGET_PROVEN
COUNTER_RECEIPT_CLEARED != AUTHORITY
```

## Receipt membrane

```text
SOURCE_VERIFIED_RECEIPT != TARGET_VERIFIED_RECEIPT
PACKET_PRESENT != PACKET_ACCEPTED
PACKET_ACCEPTED != CLAIM_ACCEPTED
ACCEPT_AS_INPUT != TARGET_PROVEN
TARGET_VERIFIED != AUTHORITY
```

## Seal

```text
TARGET_RECEIPT_RECORDS_DISPOSITION
TARGET_RECEIPT_DOES_NOT_GRANT_AUTHORITY
NONE_PROVE_THE_NEXT
```

AUTHORITY_GRANTED_BY_THIS_ARTIFACT: FALSE
