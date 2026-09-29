# CLOUDFLARE_TECHNICAL_RECEIPT_SURFACE_V0_1

Status: FROZEN V0.1
Parent: CLOUDFLARE_INFRASTRUCTURE_RAIL_V0_1
Parent commit: b156f2cd5801e0ecc85ff57d75eb7d743a39d298
Parent blob: 6fed27251dcb7ad1e134dc91e4e663a962f7684c
Authority created: FALSE
Identity binding created: FALSE
Contractual scope created: FALSE
Causal finding created: FALSE

## Purpose

Define the admissible technical-receipt shape for Cloudflare infrastructure observations without promoting infrastructure into identity, editorial authority, contractual authority, government authority, or causation.

This surface binds a schema only.

```text
TECHNICAL_RECEIPT_SURFACE = BOUND
TECHNICAL_EVENT_RECEIPTS  = EMPTY
CONTRACTUAL_SCOPE_OBJECT  = HOLD
CAUSAL_CLAIM              = HOLD
```

## Receipt classes

A future receipt MAY be classified as one of:

```text
DNS_OBSERVATION
CDN_EDGE_OBSERVATION
HTTP_RESPONSE_OBSERVATION
TLS_CERTIFICATE_OBSERVATION
WAF_OR_SECURITY_EVENT
ACCESS_EVENT
BOT_OR_CHALLENGE_EVENT
ROUTING_OR_ASN_OBSERVATION
CONFIGURATION_VERSION_RECEIPT
LOG_EXPORT_RECEIPT
RETENTION_POLICY_RECEIPT
SERVICE_STATUS_RECEIPT
OTHER_TECHNICAL_OBSERVATION
```

Classification is descriptive only and creates no authority.

## Minimum receipt schema

```json
{
  "receipt_id": null,
  "receipt_version": "V0_1",
  "parent_rail": "CLOUDFLARE_INFRASTRUCTURE_RAIL_V0_1",
  "receipt_class": null,
  "observed_at_utc": null,
  "observer": null,
  "target": {
    "hostname_or_service": null,
    "request_or_event_id": null,
    "zone_or_account_id": null,
    "ip_or_edge": null
  },
  "product_or_service": null,
  "source": {
    "source_type": null,
    "source_uri_or_reference": null,
    "source_hash": null,
    "provider_generated": null
  },
  "technical_state": {
    "http_status": null,
    "dns_result": null,
    "tls_result": null,
    "challenge_or_rule": null,
    "configuration_version": null,
    "log_fields": {}
  },
  "retention_or_export_boundary": null,
  "replay": {
    "method": null,
    "replayed_at_utc": null,
    "result": "UNPERFORMED"
  },
  "identity_binding": false,
  "legal_authority_binding": false,
  "editorial_authority": "NOT_ESTABLISHED",
  "contractual_relationship": "HOLD",
  "causal_claim": "HOLD"
}
```

Unknown or unavailable fields remain null or explicitly UNKNOWN/HOLD. They are never filled by inference.

## Admissibility rules

A technical receipt is admissible only if it preserves enough provenance to distinguish:

```text
OBSERVED_EVENT
FROM
INTERPRETATION
FROM
CONTRACTUAL_SCOPE
FROM
CAUSAL_CLAIM
```

Preferred provenance:

- provider-generated request/event identifier when available;
- UTC timestamp;
- exact hostname/service;
- exact product/service when known;
- raw or minimally transformed log/event data when lawfully available;
- source pointer;
- source hash when bytes are preserved;
- configuration/policy version when relevant;
- independent replay method when possible.

## Promotion gates

```text
LOG_PRESENT != EVENT_CAUSED_OUTCOME
HTTP_403 != SUPPRESSION_FINDING
CHALLENGE_PRESENT != POLITICAL_FILTER
DEVICE_OR_BOT_SIGNAL != NATURAL_PERSON_IDENTITY
REQUEST_METADATA != BIOMETRIC_DATABASE
EDGE_CONTROL != EDITORIAL_CONTROL
SERVICE_CONFIG != GOVERNMENT_POLICY
PROVIDER_LOG != CONTRACT
CONTRACT != GOVERNMENT_AUTHORITY
```

A receipt may prove that a technical event was observed within its scope. It does not inherit a broader conclusion.

## Replay states

```text
UNPERFORMED
MATCH
DIVERGE
INCOMPLETE
BLOCKED
CONFLICT
```

Replay result applies only to the technical receipt being replayed.

## Cross-rail membrane

```text
TECHNICAL_RECEIPT -> IDENTITY_BINDING        = BLOCKED
TECHNICAL_RECEIPT -> LEGAL_AUTHORITY         = BLOCKED
TECHNICAL_RECEIPT -> EDITORIAL_AUTHORITY     = BLOCKED
TECHNICAL_RECEIPT -> CONTRACTUAL_SCOPE       = BLOCKED
TECHNICAL_RECEIPT -> CAUSAL_FINDING          = BLOCKED
```

A separate local receipt is required for every promoted edge.

## Empty-state rule

At freeze time this surface contains no Cloudflare event instance.

```text
SCHEMA_BOUND = TRUE
EVENT_RECEIPTS_BOUND = 0
NO_EVENT_RECEIPT != NO_EVENT_OCCURRED
NO_LOG_RECEIPT != NO_LOG_EXISTS
NO_CONTRACT_RECEIPT != NO_CONTRACT_EXISTS
```

## Final freeze

```text
CLOUDFLARE_TECHNICAL_RECEIPT_SURFACE_V0_1 = FROZEN
PARENT_RAIL = CLOUDFLARE_INFRASTRUCTURE_RAIL_V0_1
EVENT_RECEIPTS = EMPTY
CONTRACTUAL_SCOPE_OBJECT = HOLD
CAUSAL_CLAIM = HOLD
AUTHORITY_CREATED = FALSE
IDENTITY_BINDING_CREATED = FALSE
```
