# RESOLUTION_RECEIPT_SCHEMA_V0

NAME: RESOLUTION_RECEIPT_SCHEMA_V0
PURPOSE: Record which bound identity governs a named conflict without erasing the other.
STATUS: SEATED / SCHEMA_ONLY
AUTHORITY_GRANTED: FALSE
FIRST_INSTANCE: COUNTER_RECEIPT_VERSION_RESOLUTION_V0
RESOLUTION_CLASS_OF_FIRST_INSTANCE: BIND_AND_HOLD

## Shape

```text
RESOLUTION_RECEIPT := {
  resolution_id              : stable_identifier
  timestamp                  : ISO8601_UTC
  conflict_class             : SAME_SHORT_NAME_DISTINCT_BYTES | BYTE_DRIFT |
                               LAYER_MISMATCH | UNDECLARED_REF | OTHER
  resolution_class           : BIND_AND_HOLD | SUPERSEDE | SPLIT_NAMESPACE | REJECT_INVALID
  identity_a                 : { short_name, surface, path_or_container, blob_or_section }
  identity_b                 : { short_name, surface, path_or_container, blob_or_section }
  relationship               : literal non-implication statement
  canonical_version          : A | B | HOLD
  supersession               : TRUE | FALSE
  deletion                   : FALSE
  rewrite                    : FALSE
  use_while_hold             : required disambiguation rule or null
  authority_granted          : FALSE
}
```

## Rules

1. `resolution_class = BIND_AND_HOLD` MAY NOT set `canonical_version` to A or B.
2. `resolution_class = SUPERSEDE` MUST set `canonical_version` to A or B and MUST leave the non-canonical identity non-deleted and non-rewritten.
3. `SAME_NAME != SAME_BYTES`.
4. `NEWER_DEFINITION != AUTOMATIC_SUPERSESSION`.
5. Missing `canonical_version` → HOLD.
6. This schema grants no authority.

AUTHORITY_GRANTED_BY_THIS_ARTIFACT: FALSE
