# Receipts Machine OS V0

**Recall name:** `RECEIPTS_MACHINE_OS_V0`  
**Role:** umbrella operating system for receipt-bounded observation, navigation, verification, replay, and rendering  
**Authority:** `FALSE`

## Purpose

`RECEIPTS_MACHINE_OS_V0` sits above Jason’s Accountability Replay Machine and provides the operating lanes around it.

It does not turn imagination, navigation, sync, reporting, or rendering into proof.

## Core rails

```text
IMAGINATION_NAVIGATION_RAIL
        ↓
OBSERVATION_RAIL
        ↓
CLAIM_INTAKE
        ↓
JASONS_ACCOUNTABILITY_REPLAY_MACHINE_V0
        ↓
RECEIPT_STATE
        ↓
RENDER_RECEIPT_GATE
```

## Imagination Navigation Rail

Purpose: allow creative exploration, scenario-building, naming, routing, hypothesis generation, and discovery without contaminating evidentiary rails.

```text
IMAGINATION = MAY_PROPOSE
NAVIGATION  = MAY_POINT
OBSERVATION = MAY_RECORD
RECEIPT     = MAY_SUPPORT
PROOF       = REQUIRES_RECEIPTS
AUTHORITY   = FALSE
```

Hard membranes:

```text
IMAGINATION != EVIDENCE
NAVIGATION != VERIFICATION
POINTER != PROOF
SCENARIO != FACT
PARODY != FINDING
IMAGE != SOURCE
SYNC_EVENT != AUTHORITY
```

An imagination object may generate a question, search target, scenario, comparison, or candidate claim. It may not promote that object into `PROVEN`.

## Accountability Replay kernel

```text
CLAIM
→ ASK
→ SOURCE
→ CHALLENGE
→ GAP
→ HOLD / CLOSE
→ REVERSAL
→ DEFENSE
→ RECEIPT
→ PASS?
   ├─ NO  → NO IMAGE
   └─ YES → RENDER IMAGE
```

`No receipt, no render.`

## Status semantics

```text
PROVEN   = required receipt set closes the exact bounded claim
HOLD     = material receipt/gap unresolved
CONFLICT = material receipts conflict
FAILED   = required evidence fails the defined test
```

A packet may split into multiple claim rails. One rail passing never promotes another rail.

## Render Receipt Gate

```text
RENDERED_IMAGE = PIPELINE_COMPLETED
RENDERED_IMAGE != PROOF
RENDERED_IMAGE != AUTHORITY
RENDERED_IMAGE != SOURCE
PROOF = UNDERLYING_RECEIPTS_ONLY
```

## Sync / storage semantics

GitHub and Google Drive writes are persistence events, not proof events.

```text
GITHUB_WRITE != CLAIM_VERIFICATION
DRIVE_WRITE != CLAIM_VERIFICATION
SYNC != CANON
COMMIT != AUTHORITY
DOC != DEPLOYMENT
```

Read-only observations remain read-only. Explicit file creation or update is a state mutation on that storage surface and must not be mislabeled as read-only sync.

## Operating relationship

```text
RECEIPTS_MACHINE_OS_V0
├── IMAGINATION_NAVIGATION_RAIL
├── JASON_WISDOM_JOURNALISM
├── JASONS_BURDEN_OF_PROOF_MACHINE
├── GARBAGE_GENERAL_OFFENSE
├── JASONS_ACCOUNTABILITY_REPLAY_MACHINE_V0
├── QUAD_ONION_MEMBRANE
└── RENDER_RECEIPT_GATE
```

## Recall phrase

**Receipts Machine OS — imagine freely, navigate openly, prove only with receipts.**

**House rule:** No receipt, no render.
