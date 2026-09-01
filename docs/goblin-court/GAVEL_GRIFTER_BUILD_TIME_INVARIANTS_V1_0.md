# Gavel Grifter — Build-Time Invariants & Ingest Pipeline v1.0

Status: LOCKED / BUILD-TIME RULES
Authority created: false
Wrongdoing inference: false
Guilt score: NOT A FIELD

Canonical schema: `schemas/gavel-grifter-tile-v1.0.schema.json`

## Six locked invariants

1. **P-MACS is only the Minnesota Appellate Courts Case Management System.** At pipeline stage 3, `source_system` must be `P-MACS` and `system_role` must be `APPELLATE_CASE_RECORD_SYSTEM`. The schema carries no misconduct semantics for P-MACS.
2. **A BJS public hit proves public existence, not full replayability.** `bjs_public_hit:true` forces `existence_state:EXIST_PUBLIC`. `PUBLICLY_REPLAYABLE` is permitted only when all eight replay-checklist fields are true. A BJS public hit with an incomplete checklist remains `PARTIALLY_REPLAYABLE`.
3. **Private annual counts are aggregate-only.** `BJS_PRIVATE_AGGREGATE` requires `official_name_as_published:null`, `bjs_public_hit:false`, `EXIST_CONFIDENTIAL`, and `CONFIDENTIAL_BY_RULE`. A named judge missing from the BJS public list does not generate an individual tile and creates no inference.
4. **`replay_note` is operational only.** It is required, non-empty, and cannot promote `cause_state`.
5. **Ingest order is fixed.** BJS public → BJS private aggregate → P-MACS → MCRO → courthouse → retention/expungement. The runner must never use a stage-4 remote miss to jump directly to a stage-6 destruction or expungement state.
6. **Red means the replay chain stopped.** It does not mean guilt, wrongdoing, corruption, or misconduct. Every tile carries `wrongdoing_inference:false`.

## Canonical ingest order

| Stage | Source | Mandatory behavior |
|---|---|---|
| 1 | BJS public discipline | Public hit sets `bjs_public_hit:true` and `EXIST_PUBLIC`. Full replay requires 8/8 checklist. |
| 2 | BJS annual private counts | Emit aggregate tile only. Never bind a private count to a named judge. |
| 3 | P-MACS | Appellate record system only. Record reversal/remand as appellate history; do not infer misconduct. |
| 4 | MCRO | Remote hit/miss only. A miss yields `EXIST_UNKNOWN`, `REMOTE_NO`, `CAUSE_UNKNOWN` until the courthouse rail is checked. |
| 5 | Courthouse | Required after an unresolved remote miss when a courthouse check is available. Record what the clerk/system actually confirms. |
| 6 | Retention / expungement receipt | Promote to `RETENTION_DESTROYED_CONFIRMED` or `EXPUNGED_CONFIRMED` only from an official receipt that establishes that cause. |

## Replay checklist

A tile can be `PUBLICLY_REPLAYABLE` only when all are true:

- `case_number`
- `parties`
- `charges`
- `procedural_history`
- `disposition`
- `judge_name`
- `written_opinion`
- `final_order`

## Neutral cause states

- `PUBLICLY_REPLAYABLE`
- `PARTIALLY_REPLAYABLE`
- `CONFIDENTIAL_BY_RULE`
- `REMOTE_BLOCKED`
- `NON_ELECTRONIC`
- `EXPUNGED_CONFIRMED`
- `RETENTION_DESTROYED_CONFIRMED`
- `CAUSE_UNKNOWN`

## Pipeline guard pseudocode

```text
stage 1: scan BJS public
stage 2: ingest BJS private aggregate counts
stage 3: query P-MACS
stage 4: probe MCRO

if stage4.access == REMOTE_NO:
    emit CAUSE_UNKNOWN
    require stage 5 before any stage-6 cause promotion

stage 5: courthouse check

if official receipt establishes expungement or retention destruction:
    stage 6: promote exact confirmed cause
else:
    preserve CAUSE_UNKNOWN / other exact access state
```

## Hard prohibitions

```text
BJS_PRIVATE_AGGREGATE -> named judge          FORBIDDEN
P-MACS -> misconduct inference                FORBIDDEN
MCRO MISS -> destroyed                        FORBIDDEN
MCRO MISS -> expunged                         FORBIDDEN
REMOTE_NO -> record does not exist            FORBIDDEN
RED CELL -> guilt/wrongdoing                   FORBIDDEN
REVERSAL -> corruption                         FORBIDDEN
```

## Build gate

Before any live ingest runner is enabled:

1. Validate the schema with a Draft 2020-12 validator.
2. Test positive and negative fixtures for each invariant.
3. Ensure stage 4 cannot promote a stage-6 cause without a stage-5/official receipt path.
4. Ensure aggregate private discipline never emits `official_name_as_published`.
5. Ensure `wrongdoing_inference` can only be `false`.
6. Preserve every source URL and exact quoted phrase used for promotion.

Core rule:

> RED = REPLAY STOP. RED != WRONGDOING.
