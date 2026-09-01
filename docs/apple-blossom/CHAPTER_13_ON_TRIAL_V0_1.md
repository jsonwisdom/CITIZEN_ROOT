# CHAPTER 13 ON TRIAL — Citizen Access Arcade v0.1

Status: SPEC / HOSTING-ACCESS AUDIT
Authority created: false
Live ingest: false
Identity bind: false
Judges scored: 0
Gavel Grifter rails changed: none

## Premise

Put Minnesota public-data access under replay, not people under accusation.

The game asks one boring question over and over:

> What did the official public-access surface actually establish?

The citizen is never required to hold a Microsoft Azure account merely because a government entity hosts systems in Azure. Legal access derives from Minnesota law and the agency's public-access duties; hosting is a separate dependency rail.

## Official legal anchor

Minn. Stat. § 13.03:

- Public government data is public unless classified otherwise by statute, temporary classification, or federal law.
- A person must be permitted to inspect and copy public government data at reasonable times and places.
- Inspection of electronic data already made available remotely includes remote access and the ability to print or download on the public's own equipment.
- The responsible authority or designee is the legal request endpoint.

Official source:
https://www.revisor.mn.gov/statutes/cite/13.03

## Hosting facts rail

Minnesota IT Services uses a multicloud strategy. The Office of the Legislative Auditor reported in 2026 that MNIT managed IaaS/PaaS assets with AWS, Microsoft Azure, and Google Cloud, and that Azure was designated the primary cloud provider.

Official audit:
https://www.auditor.leg.state.mn.us/fad/2026/fad26-04.htm

MDE separately published Azure-migration communications describing migration of Department of Education applications to Microsoft Azure Cloud and project URL/status changes.

Official MDE migration surface:
https://education.mn.gov/mdeprod/idcplg?IdcService=SS_QD_GET_RENDITION&coreContentOnly=1&dDocName=DEV042004&dID=157760

## Constitutional split

```text
LEGAL_RIGHT_TO_DATA
  !=
HOSTING_VENDOR
```

```text
CITIZEN_CLIENT
  -> public URL or Chapter 13 request
  -> agency responsible authority / designee
  -> public record or lawful classification response

HOST_STACK
  -> MNIT / Azure / AWS / Google Cloud / on-prem / unknown
```

Azure is a dependency of the state stack where used. It is not a citizen-side legal credential.

## Arcade objective

A player chooses a Minnesota public-data surface and attempts to replay the access path from the public side only.

The player wins by establishing the exact stopping point with receipts.

No motive inference. No wrongdoing score. No named-person accusation.

## Five audit flags

Each level emits exactly these five flags:

1. `LEGAL_ACCESS`
   - `PUBLIC`
   - `CLASSIFIED_BY_LAW`
   - `UNKNOWN`
   - Must include statute or official classification receipt.

2. `REMOTE_SURFACE`
   - `OPEN_HTTP`
   - `PUBLIC_PORTAL`
   - `LOGIN_REQUIRED`
   - `REMOTE_UNAVAILABLE`
   - `UNKNOWN`

3. `HOST_VENDOR`
   - `MNIT`
   - `AZURE`
   - `AWS`
   - `GOOGLE_CLOUD`
   - `ON_PREM`
   - `MULTICLOUD`
   - `UNKNOWN`
   - Hosting never changes `LEGAL_ACCESS` by itself.

4. `CUTOVER_RISK`
   - `NONE_OBSERVED`
   - `URL_CHANGED`
   - `DOWNLOAD_GAP`
   - `MIGRATION_NOTICE`
   - `SERVICE_INTERRUPTION`
   - `UNKNOWN`

5. `APPLE_BLOSSOM_DEP`
   - `PASS_HTTP_ONLY`
   - `FAIL_VENDOR_SDK_REQUIRED_FOR_PUBLIC_READ`
   - `HOLD_UNTESTED`
   - The public reader should not require Azure SDK/Entra merely to fetch public HTML or a public downloadable record.

## Level map

### Level 1 — THE FRONT DOOR

Question: Can a citizen open the official public page without a cloud-provider credential?

Input:
- official public URL

Output:
- HTTP/public-portal receipt
- `REMOTE_SURFACE`
- `APPLE_BLOSSOM_DEP`

No scraping automation is required.

### Level 2 — SHOW ME THE RULE

Question: Is the requested data public, nonpublic/private/confidential, or still unresolved under Chapter 13?

Input:
- statute / rule / agency public-access procedure

Output:
- `LEGAL_ACCESS`
- exact legal receipt

### Level 3 — FOLLOW THE BITS

Question: Where does the public-facing system appear to be hosted or routed?

Output:
- `HOST_VENDOR`
- evidence source

Hosting is descriptive only. It does not create or erase a statutory right.

### Level 4 — CUTOVER CHAOS

Question: Did a migration change URLs, downloads, authentication, or availability?

Output:
- `CUTOVER_RISK`
- old URL / new URL if officially published
- outage or migration receipt if available

### Level 5 — APPLE BLOSSOM

Question: Did the citizen-side client invent a vendor gate that the public surface did not require?

PASS:
```text
public HTTPS fetch
+ source receipt
+ no cloud-provider SDK dependency
```

FAIL:
```text
public HTML exists
but Apple Blossom refuses to read it without Azure SDK / Entra / vendor credential
```

The failure belongs to the client architecture, not the citizen.

## Player controls

- `OPEN SOURCE`
- `SHOW STATUTE`
- `SHOW HOST RECEIPT`
- `CHECK OLD URL`
- `CHECK NEW URL`
- `DOWNLOAD PUBLIC COPY`
- `BUILD REQUEST`
- `PRINT RECEIPT`
- `REPLAY`
- `AND?`

`BUILD REQUEST` drafts a Chapter 13 request for human review. It does not file or send automatically.

## Scoreboard

No guilt score. No agency-badness score.

```text
LEGAL_ACCESS_RECEIPT     0 | 1
REMOTE_SURFACE_RECEIPT   0 | 1
HOST_RECEIPT             0 | 1
CUTOVER_RECEIPT          0 | 1
CLIENT_DEPENDENCY_TEST   0 | 1
REPLAY_COMPLETE          false | true
```

A red cell means the replay stopped or the evidence is missing.

```text
RED != WRONGDOING
AZURE != LEGAL_GATE
HOSTING != CLASSIFICATION
MIGRATION != DENIAL
REQUEST != RESPONSE
```

## Machine-readable tile

```json
{
  "artifact": "CHAPTER_13_ON_TRIAL",
  "version": "0.1",
  "mode": "HOSTING_ACCESS_AUDIT",
  "jurisdiction": "MN",
  "legal_anchor": "Minn. Stat. 13.03",
  "official_url": null,
  "agency": null,
  "legal_access": "UNKNOWN",
  "remote_surface": "UNKNOWN",
  "host_vendor": "UNKNOWN",
  "cutover_risk": "UNKNOWN",
  "apple_blossom_dep": "HOLD_UNTESTED",
  "source_receipts": [],
  "replay_complete": false,
  "wrongdoing_inference": false,
  "identity_bind": false,
  "live_ingest": false,
  "authority_created": false
}
```

## Non-propagation rules

This artifact does not unlock or modify:

- Gavel Grifter identity bind
- Decoder Engine v2
- live ingest
- criminal rail
- disciplinary rail
- judicial scoring

Chapter 13 access findings remain access findings only.

## Build gate

Before any live ingest:

1. Validate one public Minnesota URL manually.
2. Save the statute receipt.
3. Save the public-surface receipt.
4. Record hosting only when supported by a source.
5. Prove Apple Blossom can read public HTML without Azure SDK/Entra dependency.
6. Keep request generation human-reviewed and unsent by default.

Core invariant:

```text
PUBLIC RIGHT -> AGENCY DUTY -> PUBLIC SURFACE / REQUEST -> RECEIPT -> REPLAY

HOSTING VENDOR stays on a separate rail.
```
