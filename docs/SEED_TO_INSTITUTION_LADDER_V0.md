# SEED_TO_INSTITUTION_LADDER_V0

PARENT: APPLE_BLOSSOM_QUAD_ONION_V0
UPSTREAM_LOCKSET: APPLE_BLOSSOM_QUAD_ONION_LOCKSET_V0
STATUS: SEATED
ROLE: DEVELOPMENTAL / SCALE-UP MAPPING
AUTHORITY: NONE_GRANTED_BY_THIS_ARTIFACT
ROOT_INVARIANT: EACH_LAYER_FEEDS_THE_NEXT / NONE_PROVE_THE_NEXT

## Purpose

Map one stable reasoning grammar from a child-sized learning object to institutional-scale records without allowing audience, scale, title, relationship, publication, or technical sophistication to create authority.

The ladder changes complexity. It does not change the membrane.

```text
COMPLEXITY_MAY_SCALE
GRAMMAR_MUST_NOT_DRIFT
SCALE != AUTHORITY
AUDIENCE != AUTHORITY
```

## Core developmental grammar

Every rung may ask the same nine questions:

```text
SEE_IT
DATE_IT
SAVE_IT
QUESTION_IT
CHECK_IT
SHOW_THE_RECEIPT
ALLOW_A_CHALLENGE
REPLAY_IT
KEEP_THE_CORRECTION
```

These questions map onto the Quad Onion:

```text
O1 EXPERIENCE
→ O2 CONTINUITY
→ O3 RECEIPT
→ O4 AUTHORITY_BOUNDARY
→ REPLAY
```

No rung may skip directly from experience, continuity, or receipt into authority.

---

# RUNG 0 — SEED / SELF

AUDIENCE: individual learner
EXAMPLE: "I planted an apple seed."

```text
EXPERIENCE
→ OBSERVE
→ RECORD_TIME
→ SAVE_OBJECT
→ ASK_WHAT_CHANGED
→ REPLAY
```

Required membrane:

```text
MEMORY != RECEIPT
BELIEF != OBSERVATION
OBSERVATION != AUTHORITY
```

Output may feed Rung 1. It does not prove Rung 1.

---

# RUNG 1 — FAMILY

AUDIENCE: child / parent / caregiver / family member
EXAMPLE: shared learning record, family agreement, household event

```text
INDIVIDUAL_OBSERVATIONS
→ SHARED_OBJECT
→ VERSION
→ RECEIPTS
→ COUNTER_RECEIPTS
→ REPLAY
```

Required membrane:

```text
LOVE != CREDENTIAL
FAMILY != ACCESS_CONTROL
PARENT != PERMANENT_ROOT_ADMIN
RELATIONSHIP != SYSTEM_AUTHORITY
```

A caregiver role may be relevant to an independently supplied authority source. The relationship alone does not create that authority.

---

# RUNG 2 — LEARNING GROUP / SCHOOL

AUDIENCE: classmates / teachers / learning programs
EXAMPLE: experiment, assignment, observation log, classroom claim

```text
FAMILY_OR_PERSONAL_OBJECT
→ TEACHABLE_OBJECT
→ METHOD
→ SOURCE_RECEIPTS
→ PEER_CHALLENGE
→ REPLAY
```

Required membrane:

```text
TEACHER_STATEMENT != RECEIPT
GRADE != TRUTH
CURRICULUM != LEGAL_AUTHORITY
SCHOOL_RECORD != GOVERNMENT_AUTHORITY
```

The ladder does not grant a school, teacher, parent, student, or AI authority over another layer.

---

# RUNG 3 — COMMUNITY

AUDIENCE: neighborhood / town / county / civic group / public audience
EXAMPLE: local history, public meeting record, shared observation, community dataset

```text
MULTI_OBSERVER_INPUT
→ NORMALIZE
→ CONTINUITY_OBJECT
→ RECEIPT_SET
→ PUBLICATION
→ COUNTER_RECEIPT
→ REPLAY
```

Required membrane:

```text
PUBLICATION != FACT
POPULARITY != VERIFICATION
CONSENSUS != AUTHORITY
COMMUNITY_NORM != LAW
```

Disagreement is represented as competing receipts or interpretations, not erased history.

---

# RUNG 4 — ORGANIZATION / CORPORATION

AUDIENCE: company / nonprofit / team / financial or technical operator
EXAMPLE: contract workflow, asset movement, deployment, policy record, transaction

```text
ENTITY
→ OBJECT
→ VERSION
→ CLAIM
→ RECEIPT
→ AUTHORITY_SOURCE_CHECK
→ EXECUTION_RECEIPT
→ OBSERVED_DELTA
→ REPLAY
```

Required membrane:

```text
CORPORATION_EXISTS != TRANSACTION_AUTHORIZED
TITLE != AUTHORITY
SIGNATURE != AUTHORITY_BY_ITSELF
AUTHORIZED != EXECUTED
EXECUTED != RECEIVED
```

O4 evaluation requires an external authority source that covers actor, action, scope, target/domain, and time.

---

# RUNG 5 — INSTITUTION / GOVERNMENT

AUDIENCE: regulated institution / court / agency / legislature / executive body / public archive
EXAMPLE: law, regulation, order, official record, appropriation, execution event

```text
SOURCE_TEXT
→ VERSIONED_RECORD
→ PROVENANCE
→ RECEIPT
→ AUTHORITY_SOURCE
→ SCOPE_TEST
→ EXECUTION_RECEIPT
→ OBSERVED_EFFECT
→ LEGAL_EFFECT_EVALUATION
→ REPLAY
```

Required membrane:

```text
BILL != LAW
LAW != EXECUTION
ANNOUNCEMENT != IMPLEMENTATION
OFFICIAL_STATEMENT != LEGAL_EFFECT
RECEIPT != INTERPRETATION
```

This artifact never decides that legal effect exists. It only requires that any legal-effect assertion identify the governing authority and the facts needed by that authority.

---

# Cross-rung promotion rule

Promotion is not automatic.

```text
RUNG_n_OUTPUT
→ CANDIDATE_INPUT_FOR_RUNG_n+1
```

Never:

```text
RUNG_n_OUTPUT
→ PROOF_OF_RUNG_n+1
```

A downstream rung must independently validate the inputs required by its own layer and scope.

## Promotion packet

```text
PROMOTION_PACKET := {
  source_object_id
  source_version_id
  source_rung
  target_rung
  receipt_refs
  counter_receipt_refs
  evidence_manifest_or_locator
  canonicalization_version
  replay_procedure_hash
  unresolved_items
  authority_refs_or_empty
}
```

Rules:

1. `unresolved_items` MUST survive promotion.
2. Missing authority references MUST remain empty; they MUST NOT be inferred from scale, title, relationship, or publication.
3. A changed object creates a new version; it does not rewrite the prior rung.
4. A challenge creates a counter-receipt and replay path; it does not erase the original observation.
5. A downstream correction may feed back upstream as a new artifact/version, never as silent historical mutation.

---

# Universal replay questions

At every rung:

```text
WHAT_WAS_OBSERVED?
WHEN?
BY_WHOM_OR_WHAT_OBSERVER?
WHAT_OBJECT_VERSION?
WHAT_RECEIPT?
WHAT_COUNTER_RECEIPT?
WHAT_CHANGED?
WHAT_REMAINS_UNRESOLVED?
WHAT_AUTHORITY_SOURCE_IF_ANY?
CAN_ANOTHER_OBSERVER_REPLAY_IT?
```

## Failure-closed states

```text
STRUCTURAL_INVALIDITY → INVALID
REQUIRED_ASSERTION_FAILURE → FAILED
MISSING_OR_UNRESOLVED_INPUT → HOLD
REPLAY_CHECKS_PASS → VERIFIED_RECEIPT
```

`VERIFIED_RECEIPT != AUTHORITY` remains absolute.

---

# Developmental front door

Apple Blossom remains the entry surface:

```text
APPLE_BLOSSOM
→ SEE_IT
→ DATE_IT
→ SAVE_IT
→ QUESTION_IT
→ CHECK_IT
→ SHOW_THE_RECEIPT
→ ALLOW_A_CHALLENGE
→ REPLAY_IT
→ KEEP_THE_CORRECTION
```

The same grammar can scale to family, school, community, organizational, financial, corporate, and government records without allowing one domain to impersonate another.

## Bottom invariant

```text
PUBLISH_THE_RECEIPT
INVITE_THE_CONTRADICTION
REPLAY_THE_SYSTEM
KEEP_THE_CORRECTION
```

AUTHORITY_GRANTED_BY_THIS_ARTIFACT: FALSE
