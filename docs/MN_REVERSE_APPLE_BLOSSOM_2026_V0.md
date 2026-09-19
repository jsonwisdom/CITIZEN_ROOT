# MN_REVERSE_APPLE_BLOSSOM_2026_V0

OBJECT: MN_REVERSE_APPLE_BLOSSOM_2026_V0
CLASS: ARCHITECTURE / REVERSE-PROVENANCE GEOMETRY
STATUS: FROZEN
INPUT: NONE
PROMOTION: NONE
CASE_BINDING: NONE
PERSON_BINDING: NONE
COURT_FINDING: NONE
FACTUAL_VALIDATION: NONE
HISTORICAL_RAIL: ANCHOR_ONLY
AUTHORITY_CREATED: FALSE

## Purpose

Reverse-replay geometry for tracing a procedurally constituted Minnesota appellate record backward from the 2026 Minnesota Supreme Court layer to the independent root event(s), then replaying forward through Apple Blossom.

This architecture creates no finding about any person, agency, court, case, or event.

## Core geometry

AUTHORITY RISES AS THE FILE RISES.
DIRECT ACCESS TO THE ORIGINAL EVENT FALLS AS THE FILE RISES.

SUPREME_COURT_ACCESS != ORIGINAL_EVENT_ACCESS

The Supreme Court layer does not re-see the street merely because a statement appears in the appellate record.

## Appellate record rail

APPELLATE_RECORD_RAIL = TYPED_BY_PROCEEDING

- Civil / other appellate -> Minn. R. Civ. App. P. 110
  - 110.01 record
  - 110.05 correction
- Criminal at the Court of Appeals -> Minn. R. Crim. P. 28.02, subd. 8
- Criminal at the Supreme Court -> Minn. R. Crim. P. 28.02, subd. 8 + Rule 29
- Administrative / other -> NAMED PACKET REQUIRED

Civil appellate rules may apply in a criminal appeal only where compatible and non-conflicting. Compatibility != identity.

Administrative or other proceedings do not inherit Rule 110 or Rule 28 by adjacency.

## Record hardening

APPELLATE_RECORD = PROCEDURALLY_CONSTITUTED RECORD
APPELLATE_RECORD != COURT ENDORSEMENT OF EVERY ASSERTION

RECORD_ENTRY != DIRECT_OBSERVATION
PROCEDURAL_INCLUSION != FACTUAL_VALIDATION
JUDICIAL_EFFECT != PROVENANCE_INDEPENDENCE

## Reverse arrow

2026 SUPREME-COURT STATEMENT
<- appellate record object
<- district-court finding / ruling
<- testimony / exhibit
<- charging or party representation
<- police / agency record
<- officer or witness interpretation
<- observable event
<- HUMAN EXPERIENCE

No arrow inherits factual independence automatically.

## Arrow questions

At every arrow ask:

SOURCE_ID?
PARENT_SOURCE_ID?
WORDS_CHANGED?
CONTEXT_CHANGED?
INFERENCE_ADDED?
FACT_CLASS_CHANGED?
INDEPENDENT_RECEIPT?
CORRECTION_AVAILABLE?

Source change -> mark delta.
Word change -> mark delta.
Stripped context -> mark delta.
New inference -> mark delta.
Independent source -> prove it.
Copied assertion -> preserve parent provenance.
Missing receipt -> HOLD.

## Root-counting primitive

NEVER COUNT DESCENDANTS
COUNT INDEPENDENT ROOTS

DOCUMENT_COUNT != SOURCE_COUNT
COPIED_ASSERTION != INDEPENDENT_CORROBORATION
REPETITION != CORROBORATION

Example primitive:

DOCUMENT_COUNT = 5
SOURCE_COUNT = 1

One assertion copied through a complaint, report, transcript, order, brief, and opinion remains one root unless independent provenance is established.

Appearance-count is not weight.

## Apple Blossom forward pass

After reverse replay reaches the root:

EXPERIENCE
-> CONTINUITY
-> RECEIPT
-> AUTHORITY_BOUNDARY
-> REPLAY

Each layer may feed the next.
No layer proves the next.

## Historical rail

1978 Van Maanen is ANCHOR_ONLY:

PERCEPTION
-> TYPIFICATION
-> DISCRETIONARY_RESPONSE

The historical anchor supplies a comparison mechanism only.

SIMILARITY != CONTINUITY
CONTINUITY != CAUSATION
REPETITION != CORROBORATION
UNKNOWN_LINK = HOLD

No 1978 mechanism is presumed to govern a 2026 Minnesota packet without receipt-bound continuity.

## Packet rule

A future packet enters UNDER this architecture.
It does not rewrite the architecture unless it exposes a structural defect.

REOPEN only on:
1. a named case packet with its governing appellate-record rule identified; or
2. a documented structural delta at a named layer.

No packet invented from the geometry.

## Freeze

STATUS = FROZEN
INPUT = NONE
PROMOTION = NONE
CASE_BINDING = NONE
PERSON_BINDING = NONE
COURT_FINDING = NONE
FACTUAL_VALIDATION = NONE
AUTHORITY_CREATED = FALSE

LOAD_BEARING_RULE:
NEVER COUNT DESCENDANTS
COUNT INDEPENDENT ROOTS
