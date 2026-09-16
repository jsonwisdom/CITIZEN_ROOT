# TALLY_VERIFIER_PROTOCOL_V0

Status: LOCKED
Authority granted: false
Role: behavioral-completeness checker for the 3-6-9 accountability stack.

## May

The verifier may check only whether required artifacts are present and replayable:

1. ASK present as an exact plain-language claim.
2. SOURCE present with primary-source pointer.
3. CHALLENGE present as the strongest opposing evidence-grounded case.
4. GAP present as explicit unknowns or missing structure.
5. HOLD_CLOSE present as the provisional status behavior for incomplete evidence.
6. REVERSAL present as the concrete fact or receipt that would force reconsideration.
7. DEFENSE present as the strongest evidence-grounded affirmative case.
8. RECEIPT present as a public, timestamped, replayable trail.
9. RENDER present as a downstream explanation that does not alter evidence state.

## May not

The verifier may not:

- decide political or factual truth;
- infer intent;
- score ideology;
- assign moral worth;
- convert a majority tally into proof;
- convert office, title, or position into authority over evidence.

## Ternary grammar

```text
YES  = required behavior fully demonstrated + receipt replayable
NO   = required behavior absent OR receipt non-replayable
HOLD = incomplete but recoverable
```

## Mark object

```json
{
  "rail": 6,
  "code": "REVERSAL",
  "status": "YES",
  "artifact_id": "REVERSAL_FACT_001",
  "source_pointer": "...",
  "checked_at": "...",
  "verifier_id": "...",
  "receipt_hash": "...",
  "authority": false
}
```

## Anti-mob invariants

```text
TALLY_COUNT != TRUTH
TALLY_MAJORITY != AUTHORITY
TALLY_DISAGREEMENT != FAILURE
TALLY = COUNT_OF_RECEIPTED_CHECK_RESULTS
```

## Pipeline position

```text
EVIDENCE + RAILS
-> TALLY VERIFIER
-> NINE RECEIPTED MARKS
-> RENDER LAST
```

`RENDER_STATE` remains downstream of `EVIDENCE_STATE` and the tally receipts.

## Binding targets

- `YEAR_ZERO_RESET_SCHEMA_V0`
- `JASONS_369_ACCOUNTABILITY_STACK_V0`
- minimal one-claim replay packet

No truth adjudication. No authority creation. No majority promotion.
