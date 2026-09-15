# IMA-0001 RUN-0001: Canon-to-Application Architecture Mapping

## Metadata
- **Machine ID**: IMA-0001
- **Run ID**: RUN-0001
- **Domain Ruleset**: Canon-to-Application Architecture Mapping v0.1
- **Mapper**: jaywisdom.eth
- **Authority Pointer**: jaywisdom.base.eth
- **Repository Authority**: false
- **Deterministic Seed**: 0
- **Input Hash**: 8a0f0b3eb5f22555a5c297ab9cf0f2cb05410d8ac720617c1f66c98de70215e1

## Classified Canons
| Canon ID | Statement | Role |
|----------|-----------|------|
| APPLE-CANON-001 | Protect the user. | doctrine |
| APPLE-CANON-002 | Authenticate every executable link. | mechanism |
| APPLE-CANON-003 | Integration outranks modular freedom. | doctrine |
| APPLE-CANON-004 | Participation requires rule compliance. | constraint |
| APPLE-CANON-005 | A signature proves integrity, not truth. | doctrine |
| ZORA-CANON-001 | Preserve the originating creator identity. | doctrine |
| ZORA-CANON-002 | Resolve the pointer before interpreting it. | mechanism |
| ZORA-CANON-003 | Content and market object remain distinguishable. | doctrine |
| ZORA-CANON-004 | Gaps become branches, never silent corrections. | mechanism |
| ZORA-CANON-005 | Hashes preserve claims without creating authority. | doctrine |

## Accepted Hypotheses
*(Ordered by primary role, then by canonical UTF-8 byte order of hypothesis_id)*

### HYP-AC001-AC002
- **Doctrine**: Protect the user.
- **Mechanism**: Authenticate every executable link.
- **Testable Application**: A system that blocks unauthenticated links to ensure user safety.
- **Constraint**: Participation requires rule compliance.
- **Citations**: `APPLE-CANON-001`, `APPLE-CANON-002`, `APPLE-CANON-004`

### HYP-AC005-ZC004
- **Doctrine**: A signature proves integrity, not truth.
- **Mechanism**: Gaps become branches, never silent corrections.
- **Testable Application**: An audit trail that explicitly logs signature verification failures as open branches rather than auto-correcting them.
- **Constraint**: AUTHORITY_CREATED must remain false.
- **Citations**: `APPLE-CANON-005`, `ZORA-CANON-004`, `CONSTRAINT-0`

### HYP-ZC001-ZC002
- **Doctrine**: Preserve the originating creator identity.
- **Mechanism**: Resolve the pointer before interpreting it.
- **Testable Application**: A provenance graph that traces content back to the original creator via resolved pointers.
- **Constraint**: Do not equate a hash with truth, ownership, identity, copyright, or economic value.
- **Citations**: `ZORA-CANON-001`, `ZORA-CANON-002`, `CONSTRAINT-3`

### HYP-ZC003-AC002
- **Doctrine**: Content and market object remain distinguishable.
- **Mechanism**: Authenticate every executable link.
- **Testable Application**: A marketplace interface that separately authenticates the asset link and the market listing link.
- **Constraint**: Do not mutate the sealed Oxford Gambit artifacts.
- **Citations**: `ZORA-CANON-003`, `APPLE-CANON-002`, `CONSTRAINT-5`

### HYP-ZC005-ZC004
- **Doctrine**: Hashes preserve claims without creating authority.
- **Mechanism**: Gaps become branches, never silent corrections.
- **Testable Application**: A verification system that logs hash mismatches as explicit branches without claiming authoritative correction.
- **Constraint**: AUTHORITY_CREATED must remain false.
- **Citations**: `ZORA-CANON-005`, `ZORA-CANON-004`, `CONSTRAINT-0`

## Rejected Branches
- **HYP-AC003-ZC002**: Requires invented definition of 'integration' and 'modular freedom' not present in input, violating rule 8 (Reject hypotheses requiring invented evidence).

## Validation Report
- [x] All ten input canons appear exactly once in the output map.
- [x] Every accepted hypothesis references at least one canon_id.
- [x] Every source statement remains byte-identical to its preserved input form.
- [x] Every ambiguity or unsupported inference is represented as a branch or rejection.
- [x] Output ordering follows the declared deterministic ordering rule.
- [x] Replaying the canonical input with the same ruleset produces semantically identical output.
- [x] All emitted JSON artifacts parse successfully.
- [x] Every artifact receives a SHA-256 digest.
- [x] AUTHORITY_CREATED equals false.
- [x] No repository merge or default-branch mutation occurs.
