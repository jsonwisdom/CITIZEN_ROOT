# Pack 08 — CITIZEN_ROOT Replay Packet V0.1

Status: PACKAGE_SPEC
Authority: false

CITIZEN_ROOT stores pointers, derived leaves, hashes, equations, status, and limits. It should not duplicate source evidence merely for convenience.

~~~text
MONEY_REPLAY_PACKET/
  manifest.json
  source_pointers.json
  claim_atoms.json
  math.json
  receipts.json
  limits.md
  public_explanation.md
~~~

Replay:

~~~text
1. Resolve source pointers.
2. Verify source hashes where available.
3. Confirm jurisdiction and period.
4. Rebuild money classifications.
5. Recompute every equation.
6. Compare machine values.
7. Recheck required bridges.
8. Preserve HOLD / PASS / CONFLICT.
9. Rebuild public explanation.
~~~

CITIZEN_ROOT law:

~~~text
POINTER != SOURCE
DERIVED_LEAF != SOURCE_ARTIFACT
REPLAY_MATCH != POLICY_ENDORSEMENT
MATH_PASS != POLITICAL_VERDICT
ROOT_INDEX != AUTHORITY
~~~

Correction:

~~~text
OLD_PACKET
→ PRESERVE
→ APPEND_CORRECTION
→ LINK_SUPERSEDING_PACKET
→ REPLAY
~~~
