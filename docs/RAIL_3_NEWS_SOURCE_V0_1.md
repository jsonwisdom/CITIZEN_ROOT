# RAIL 3 — NEWS SOURCE V0.1

**Object ID:** `RAIL_3_NEWS_SOURCE_V0_1`  
**Class:** `NEWS_SOURCE_PROVENANCE_RAIL`  
**Root:** `jsonwisdom/CITIZEN_ROOT`  
**Root pointer:** `CITIZEN_ROOT_INDEX.json#artifact_registry.entries[id=RAIL_3_NEWS_SOURCE_V0_1]`  
**Prior hold receipt:** `docs/RAIL_3_UNDEFINED_HOLD_RECEIPT_V0_1.md`  
**Definition status:** `GENERATED`  
**Authority:** `false`

## Purpose

Record what a news source published, who or what it attributed, and which primary materials it linked. This rail preserves source provenance. It does not independently prove the reported event, legal conclusion, intent, causation, or authority.

## Required source record

```text
SOURCE_ID
OUTLET
AUTHOR_OR_BYLINE
HEADLINE
CANONICAL_URL
PUBLISHED_AT
UPDATED_AT
ACCESSED_AT
SOURCE_TYPE
CLAIM_UNIT
ATTRIBUTION
EXACT_QUOTE_OR_PARAPHRASE
PRIMARY_SOURCE_LINKS
CORRECTION_OR_RETRACTION_STATE
ARCHIVE_OR_CONTENT_HASH
```

Use `null` or `HOLD` when a value is not available. Never manufacture metadata to close a record.

## Source types

- `NEWS_REPORT`
- `TRANSCRIPT`
- `INTERVIEW`
- `ANALYSIS`
- `OPINION`
- `PRESS_RELEASE`
- `LIVE_BLOG`
- `CORRECTION`

## Claim states

| State | Meaning |
|---|---|
| `OBSERVED` | The source surface was opened and the identified content was present. |
| `SOURCE_ANCHORED` | A claim unit is tied to a URL, date, attribution, and retrievable passage. |
| `PRIMARY_LINKED` | The source links to an opened primary artifact supporting the attribution. |
| `CONFLICT` | Another sourced record materially contradicts the claim unit. |
| `CORRECTED` | The publisher issued a visible correction or replacement. |
| `RETRACTED` | The publisher withdrew the content. |
| `HOLD` | A required receipt, attribution, passage, or accessible source is unresolved. |

## Replay sequence

```text
IDENTIFY_SOURCE
→ CAPTURE_METADATA
→ EXTRACT_CLAIM_UNIT
→ CLASSIFY_QUOTE_OR_PARAPHRASE
→ RESOLVE_ATTRIBUTION
→ OPEN_PRIMARY_LINKS
→ CHECK_CORRECTIONS
→ SEEK_COUNTER_SOURCE
→ ASSIGN_STATE
→ EMIT_RECEIPT
```

## Separation membrane

```text
SOURCE_EXISTS
!=
SOURCE_CLAIM_IS_TRUE
!=
UNDERLYING_EVENT_PROVEN
!=
LEGAL_EFFECT
!=
CAUSATION
!=
AUTHORITY
```

News-source reporting may anchor what was published and attributed. Promotion of an underlying claim requires the appropriate independent receipt or a separate primary-source rail.

## Invariants

- `REGISTER_SHAPE != TRUTH`
- `HEADLINE != FULL_ARTICLE`
- `ARTICLE != PRIMARY_SOURCE`
- `QUOTE != CONTEXT_COMPLETE`
- `ATTRIBUTION != CORROBORATION`
- `MULTIPLE_OUTLETS != MULTIPLE_INDEPENDENT_SOURCES`
- `PRIMARY_LINKED != PRIMARY_PROVEN`
- `CORRECTION != ORIGINAL_NEVER_EXISTED`
- `SOURCE_ANCHORED != FACT_PROVEN`
- `RAIL_3 != VERDICT_RAIL`
- `AUTHORITY = FALSE`

## Root-link rule

Every downstream `RAIL_3` receipt must point to this definition and to its own source record. The Citizen Root pointer is navigation and discovery, not evidentiary promotion or authority.
