# APPLE_BLOSSOM_QUAD_ONION_LOCKSET_V0

ARTIFACT_SET: APPLE_BLOSSOM_QUAD_ONION_V0
STATUS: SEATED + EXTENSION
AUTHORITY: NONE_GRANTED_BY_THIS_ARTIFACT
ROOT_INVARIANT: EACH_LAYER_FEEDS_THE_NEXT / NONE_PROVE_THE_NEXT

## Selected next locks

1. COUNTER_RECEIPT_PROTOCOL_V0
2. AUTHORITY_BOUNDARY_V0
4. QUAD_ONION_REPLAY_ENGINE_V0
5. CONTINUITY_OBJECT_SCHEMA_V0

SEED_TO_INSTITUTION_LADDER_V0 remains the next developmental/presentation layer after the core mechanics close.

## Replay-closure correction

`RECEIPT_SCHEMA_V0` contains hashes and a replay seed, but a digest or seed alone cannot reconstruct arbitrary evidence bytes. Therefore exact replay is conditional until the receipt chain also binds the evidence location/manifest and the replay procedure.

Required replay closure fields:

- `hash_alg`
- `canonicalization_version`
- `evidence_manifest_or_locator`
- `replay_procedure_hash`

Invariant:

`HASH_PROVES_IDENTITY != HASH_RECONSTRUCTS_CONTENT`

Until those fields are available and resolvable:

`REPLAY_SAFE = CONDITIONAL`

This does not grant authority and does not invalidate the receipt as an observation record.

---

# ARTIFACT 5 — COUNTER_RECEIPT_PROTOCOL_V0

NAME: COUNTER_RECEIPT_PROTOCOL_V0
PARENT: RECEIPT_SCHEMA_V0
LAYER: O3 — RECEIPT
AUTHORITY: NONE

## Purpose

A counter-receipt challenges a receipt without deleting history, rewriting the challenged bytes, or automatically proving the counter-claim.

## Shape

```text
COUNTER_RECEIPT := {
  counter_id              : UUID_v7 | deterministic_hash
  challenged_receipt_id   : receipt_id
  timestamp               : ISO8601_UTC
  observer_id             : opaque_identifier
  challenge_type          : EVIDENCE_MISMATCH | CLAIM_SCOPE | CLOCK_CONFLICT |
                            CHAIN_CONFLICT | BINDING_MISMATCH | REPLAY_FAILURE |
                            AUTHORITY_OVERREACH | OTHER
  challenge_digest        : hash(COUNTER_CLAIM)
  counter_evidence_digest : hash(COUNTER_EVIDENCE)
  divergence_point        : receipt_id | version_id | step_id
  prior_counter_receipts  : [hash...]
  replay_procedure_hash   : hash(PROCEDURE)
  signature_or_null       : optional_cryptographic_sig
}
```

## Protocol

```text
COUNTER_RECEIPT_ARRIVES
→ MARK_CHALLENGED_RECEIPT_HELD_BY_INDEX_EVENT
→ FREEZE_DIVERGENCE_POINT
→ REVERSE_REPLAY
→ COMPARE ORIGINAL / COUNTER EVIDENCE
→ {CONFIRM_ORIGINAL | CORRECT | HOLD}
→ EMIT RESOLUTION_RECEIPT
→ APPEND NEW ARTIFACT VERSION IF CONTENT CHANGES
```

The challenged receipt body is not rewritten. Lifecycle changes are index events so byte identity remains stable.

Invariants:

`COUNTER_RECEIPT != REFUTATION`

`CHALLENGE != FALSE_CLAIM`

`CORRECTION != DELETION`

`UNRESOLVED_COUNTER -> HOLD`

---

# ARTIFACT 6 — AUTHORITY_BOUNDARY_V0

NAME: AUTHORITY_BOUNDARY_V0
PARENT: APPLE_BLOSSOM_QUAD_ONION_V0
LAYER: O4 — AUTHORITY BOUNDARY
AUTHORITY: NONE CREATED BY THIS SCHEMA

## Boundary chain

```text
OBSERVED
!= AUTHORIZED
!= EXECUTED
!= RECEIVED
!= LEGAL_EFFECT
```

No O3 receipt may promote itself into O4.

## Authority predicate

An authority assertion may be evaluated only when the record identifies, at minimum:

```text
AUTHORITY_CANDIDATE := {
  actor_id
  authority_source_ref
  authority_source_digest
  scope
  permitted_action
  effective_time_window
  target_or_domain
  delegation_chain_or_null
}
```

`AUTHORIZED(action)` may be emitted only if the supplied authority source actually covers the actor, action, scope, target/domain, and relevant time.

Even then:

`AUTHORIZED != EXECUTED`

Execution requires an execution receipt. Receipt/credit/delivery requires its own observation. Legal effect, where applicable, requires the governing rule and facts that trigger it; it is never inferred merely from a receipt or execution event.

Prohibitions:

- title, role, relationship, possession, publication, signature, token, or account access alone MUST NOT establish authority;
- parent/family relationship MUST NOT silently become permanent system authority;
- corporate existence MUST NOT establish authority for a transaction;
- observation MUST NOT establish legal effect.

---

# ARTIFACT 7 — CONTINUITY_OBJECT_SCHEMA_V0

NAME: CONTINUITY_OBJECT_SCHEMA_V0
PARENT: APPLE_BLOSSOM_QUAD_ONION_V0
LAYER: O2 — CONTINUITY / BLOSSOM
AUTHORITY: NONE

## Shape

```text
CONTINUITY_OBJECT := {
  object_id                : stable_identifier
  version_id               : deterministic_hash
  parent_version_id        : version_id | null
  created_at               : ISO8601_UTC
  observer_id              : opaque_identifier
  content_digest           : hash(CANONICAL_CONTENT)
  change_set_digest        : hash(DELTA_FROM_PARENT)
  source_receipts          : [receipt_id...]
  canonicalization_version : identifier
  status_event_refs        : [event_id...]
}
```

Rules:

1. `object_id` persists across versions; `version_id` does not.
2. A version is immutable after emission.
3. A content change creates a new `version_id`.
4. Lifecycle/status change emits a status/index event and does not rewrite version bytes.
5. Parent links are append-only and acyclic.
6. Missing history is `HOLD`, not silently filled from memory.

Required replay views:

```text
HISTORICAL_STATE
CURRENT_STATE
COUNTERFACTUAL_CURRENT_RULES_STATE
```

These views MUST remain distinguishable.

`MEMORY != CONTINUITY_RECEIPT`

`CURRENT_RULES != HISTORICAL_RULES`

---

# ARTIFACT 8 — QUAD_ONION_REPLAY_ENGINE_V0

NAME: QUAD_ONION_REPLAY_ENGINE_V0
PARENT: APPLE_BLOSSOM_QUAD_ONION_V0
LAYERS: O1 → O2 → O3 → O4
AUTHORITY: NONE

## Inputs

```text
REPLAY_INPUT := {
  object_version
  receipt_chain
  counter_receipt_set
  evidence_manifest
  replay_procedure_hash
  canonicalization_version
  authority_refs_or_empty
}
```

## Deterministic pipeline

```text
1 FREEZE_INPUTS
2 VALIDATE_CONTINUITY
3 VALIDATE_RECEIPT_SHAPE
4 RESOLVE_EVIDENCE
5 RECOMPUTE_DIGESTS_AND_BINDINGS
6 APPLY_COUNTER_RECEIPTS
7 REPLAY_CLAIM_PROCEDURE
8 EVALUATE_O4_SEPARATELY_IF_REQUESTED
9 EMIT_RESULT + TRACE
```

## Result precedence

```text
STRUCTURAL_INVALIDITY → INVALID
DIGEST / BINDING / REQUIRED_ASSERTION_FAILURE → FAILED
MISSING_INPUT / UNRESOLVED_COUNTER / UNRESOLVED_DEPENDENCY → HOLD
ALL_REQUIRED_REPLAY_CHECKS_PASS → VERIFIED_RECEIPT
```

`VERIFIED_RECEIPT` means the defined receipt/evidence procedure replayed successfully. It does not mean authority, execution, receipt by another party, legal effect, intent, or universal truth.

O4 is evaluated independently and can remain `NOT_EVALUATED` or `HOLD` even when O3 is verified.

## Trace requirement

Every run emits a deterministic trace containing input identifiers, procedure version/hash, step outcomes, divergence point if any, and final result. A new engine/procedure version creates a new replay identity rather than mutating the old one.

## Global invariants

```text
TOKEN       != EVIDENCE
CAST        != AUTHORITY
PUBLICATION != FACT
BILL        != LAW
LAW         != EXECUTION
RECEIPT     != INTERPRETATION
OBSERVATION != AUTHORITY
CORRECTION  != FAILURE
```

## Bottom rule

```text
PUBLISH_THE_RECEIPT
INVITE_THE_CONTRADICTION
REPLAY_THE_SYSTEM
KEEP_THE_CORRECTION
```

---

# Lock order

```text
ROOT_INVARIANT_CHARTER_V0
→ DEVELOPMENTAL_GRAMMAR_V0
→ APPLE_BLOSSOM_QUAD_ONION_V0
→ RECEIPT_SCHEMA_V0
→ CONTINUITY_OBJECT_SCHEMA_V0
→ COUNTER_RECEIPT_PROTOCOL_V0
→ AUTHORITY_BOUNDARY_V0
→ QUAD_ONION_REPLAY_ENGINE_V0
→ SEED_TO_INSTITUTION_LADDER_V0 (NEXT DEVELOPMENTAL LAYER)
```

AUTHORITY_GRANTED_BY_THIS_SET: FALSE
