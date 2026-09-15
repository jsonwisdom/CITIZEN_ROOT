# Jay's GitHub as a Service for the Public — v0.1

**Root:** `jsonwisdom/CITIZEN_ROOT`  
**Builder:** `jsonwisdom`  
**Authority:** `false`

## Purpose

Make Jay's GitHub estate usable as a public verification service without collapsing public, private, family, secret, and proof boundaries.

```text
PUBLIC   -> discoverable repository + public artifact pointers
PROOF    -> receipt/hash/commit/source-anchor surfaces
FAMILY   -> routing pointers only; identity/consent do not inherit
PRIVATE  -> existence may be counted publicly; names/content stay private
SECRET   -> slot/policy may be indexed; secret values are never indexed
```

## Public request path

```text
QUESTION
  -> CITIZEN_ROOT
  -> REPOSITORY_SERVICE_INDEX
  -> SOURCE REPOSITORY / ARTIFACT
  -> RECEIPT / COMMIT / HASH / PRIMARY SOURCE
  -> REPLAY
  -> VERIFIED | HOLD | CONFLICT
```

`SYSTEM_OUTPUT != AUTHORITY`

`MISSING_RECEIPT -> HOLD`

`SEARCH_MISS != NO_WORK`

## Visibility membrane

1. Public repositories may be indexed by name and URL.
2. Private repositories are not named in the public catalog. The public catalog exposes only the private-repository count and the fact that a private control plane exists.
3. Family routing is pointer-only. Repository names do not prove genealogy, identity, consent, custody, ownership, school status, or authority.
4. Secret material is never copied into this repository. A secret registry may describe a required secret class or external vault location, but never a credential, token, key, seed phrase, password, or secret value.
5. Proof artifacts should prefer immutable identifiers: commit SHA, git blob SHA, SHA-256 digest, source URL, page/finding anchor, and timestamp when available.

## Service classes

### Civic / public research

Use `CITIZEN_ROOT` as the discovery root, then follow pointers into civic and jurisdiction-specific repositories such as `mn-ago-entropy-ledger`, `AL`, `COMPUTERWISDOM`, `JOY`, and other public surfaces.

### Proof / replay

Primary proof-oriented surfaces include `public-proof`, `prooflayer-repo`, `provenance-audit-kit`, `receipts-engine-v1`, `receiptos-base`, `ReceiptOS`, `receiptos-replay-proof`, `verifygate`, and the root receipts under `CITIZEN_ROOT`.

### Family

Family artifacts remain independently addressable through their source repositories and the protected routing membrane in `JOY`. Shared routing never creates shared identity or inherited consent.

### Private

Private repository names and Drive pointers are held in the private control-plane index. Public users receive only a redacted boundary receipt.

### Secrets

Secrets are **not data for this public service**. Only safe descriptors such as `required=true`, `provider`, `rotation_state`, or `vault_pointer_present=true` may be indexed in a private control plane. Secret values remain outside Git history.

## Current inventory boundary

```text
TOTAL_GITHUB_REPOSITORIES = 87
PUBLIC_REPOSITORIES       = 80
PRIVATE_REPOSITORIES      = 7
PUBLIC_PRIVATE_NAMES      = REDACTED
SECRET_VALUES_INDEXED     = 0
AUTHORITY_CREATED         = FALSE
```

The machine-readable public inventory is `registry/REPOSITORY_SERVICE_INDEX_V0_1.json`.

## Public contract

This service is for discovery and verification, not adjudication.

```text
CLAIM != PROOF
REPOSITORY != PERSON
POINTER != EVIDENCE
MIRROR != ORIGINAL
PUBLIC_RECORD != CRIMINAL_JUDGMENT
DRIVE_DOC != ORIGINAL_GITHUB_BYTES
```

A citizen should be able to start with a question, locate the relevant public artifact, reproduce the receipt chain, and see exactly where the record closes or remains on HOLD.
