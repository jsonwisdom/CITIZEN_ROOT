# claim_status

Append-only status changes only.

Original claim leaf is never deleted.
Status history is preserved forever via new leaves that point back to the original.

CLAIM → challenged → evidence → adjudication/status → immutable history
