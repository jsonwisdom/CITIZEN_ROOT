# NIGHT WOLFE — ADVERSARIAL AUDIT CORRECTION V0.1

**Object ID:** `NIGHT_WOLFE_ADVERSARIAL_AUDIT_CORRECTION_V0_1`  
**Snapshot:** 2026-09-16 UTC  
**Status:** `DO_NOT_FREEZE`  
**Posture:** `WATCH_ONLY_CHAIN`  
**Authority:** `false`  
**Purpose:** Correct the prior adversarial report without erasing its historical record.

## Source boundary

Chain findings below were independently rechecked against Base RPC transaction receipt, contract calls, runtime bytecode, BaseScan, and Blockscout. Human-network findings retain their individual evidence classifications. No entity is merged because of name, imagery, nationality, marriage, or thematic resemblance.

## 1. Corrected on-chain replay

| Field | Corrected finding |
|---|---|
| Contract | `0xe75b1EB7cdFdcE0bF0329FECEBa021DD5bE62A5C` |
| Creation transaction | `0x8a4bf50d040960b1a738eb243515215a1cd7611139b4ed75ac3ddffe93f981e1` |
| Proxy pattern | EIP-1167 minimal proxy |
| Implementation | `0x5DbD43785954D43c1643A0caf2ecEf9E0056Ff13` |
| Implementation class | Zora `ContentCoin` |
| Name / symbol | `NIGHT WOLF 💒` / `NIGHTJR` |
| Decimals | `18`, returned directly by `decimals()` |
| Total supply | `1,000,000,000 NIGHTJR` |
| Outer sender | `0x8D47bA07Ff9ccCCF58c7E8810eE42c0Dc8B8b123`; bundler transaction sender, not proven creator |
| Creator/referrer roles | `HOLD` pending ABI-specific decoding |
| Creation-transaction swap | No `Swap` event observed inside the creation transaction |
| Later market activity | `HOLD`; later blocks not yet searched |

### Transfer path

1. `0x0 → TOKEN_CONTRACT`: 1,000,000,000 NIGHTJR.
2. `TOKEN_CONTRACT → 0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2`: 10,000,000 NIGHTJR.
3. `TOKEN_CONTRACT → 0x0469a4Bd3724DC86C9542F4694c976DA13C450c0`: 990,000,000 NIGHTJR.
4. `0x0469a4Bd3724DC86C9542F4694c976DA13C450c0 → 0x498581fF718922c3f8e6A244956aF099B2652b2b`: approximately 990,000,000 NIGHTJR.

The 990M entries describe one continuing path through the intermediate hook address into the Uniswap V4 Pool Manager. They are not two independent allocations.

### Chain close

`NIGHTJR` is a Zora ContentCoin deployed through an EIP-1167 minimal proxy. No decoded transaction, transfer, creator, referrer, or pool edge establishes a human-identity join to Donald Trump Jr., Umar Kremlev, the Night Wolves, or another Russian entity.

`TOKEN → HUMAN_NETWORK = NOT_PROVEN`

Off-chain metadata that has not been independently opened is not treated as cleared.

## 2. Corrected relationship graph

| Edge | Classification | Receipt boundary |
|---|---|---|
| Don Jr. → Kremlev | DOCUMENTED | Couple acknowledged Kremlev hosted two celebration nights and described him as a friend |
| Bettina → Kremlev | DOCUMENTED | Same joint statement |
| Kremlev → Night Wolves | REPORTED | Journalistic sourcing; no primary membership roster opened |
| Night Wolves → Rubezhnoi | REPORTED | Proekt-derived reporting; underlying primary document not opened |
| Rubezhnoi → Putin security apparatus | DOCUMENTED | Reported office: Presidential Security Service within FSO |
| Kremlev → Putin | REPORTED | Order of Friendship and delegation reporting do not establish a directive |
| Gazprom → IBA | DOCUMENTED / HISTORICAL | Partnership began in April 2021 and ended December 31, 2022 |
| Gazprom → IB Challenger | HOLD | No direct fund trace |
| IB Challenger → wedding vendors | REPORTED / SOURCE-ANCHORED | ProPublica reports payments through a Dubai-based IBA-affiliated entity |
| Russian state → payment order | NOT_PROVEN | No order, directive, reimbursement, or account trace |
| NIGHTJR → Don Jr. | NOT_PROVEN | No decoded on-chain identity join |
| NIGHTJR → Russian entity | NOT_PROVEN | No decoded on-chain identity join |

## 3. Spouse precision

- Bettina Anderson/Trump is described by Project Paradise as a Palm Beach native active in Florida conservation.
- No sourced Russia connection for Bettina was established in this audit.
- Exact birth date, Columbia degree, and specific business claims remain outside the frozen record until primary receipts are opened.
- Melania Trump was born in Slovenia, then part of Yugoslavia.
- Slovenia is not Russia or Uzbekistan.
- Nationality, foreign birth, and marriage do not establish state affiliation.

## 4. Dated edge ledger

| Date | Edge | Class |
|---|---|---|
| 2021-04 | Gazprom → IBA general partnership | DOCUMENTED / HISTORICAL |
| 2022-12-31 | Gazprom → IBA contract ended | DOCUMENTED / HISTORICAL |
| 2026-05 | Kremlev → Don Jr./Bettina celebration benefit | DOCUMENTED |
| 2026-09-14 | ProPublica reports Dubai-entity payment path | REPORTED / SOURCE-ANCHORED |
| 2026-09-15 | Couple confirms friendship and celebration gift | DOCUMENTED |
| 2026-09-15 | Congressional inquiry announced | DOCUMENTED EVENT; allegations are not findings |

## 5. Money-flow ledger

| Flow | State |
|---|---|
| Token mint → contract → 10M allocation + 990M pool path | ON-CHAIN PROVEN |
| Kremlev / affiliated Dubai entity → vendors | REPORTED / SOURCE-ANCHORED |
| Personal funds versus organizational funds | HOLD |
| Gazprom → IB Challenger | HOLD |
| Russian state → payment direction | NOT_PROVEN |
| Payment → quid pro quo | NOT_PROVEN |

## 6. Missing receipts

1. ABI-specific role decode for `0x829Adf...` and `0x694ce...`.
2. Later-block search for external swaps.
3. Primary Night Wolves membership record for Kremlev.
4. Underlying Proekt evidence for the Zaldostanov–Rubezhnoi introduction.
5. Vendor invoices or bank records separating personal from organizational funds.
6. Russian state order, reimbursement, or payment instruction.
7. Communications concerning Don Jr. or the celebration involving Kremlev and state/security officials.
8. Direct OFAC and EU sanctions-list checks for Kremlev at the relevant snapshot.
9. Primary receipts for Bettina’s exact birth date and education.
10. Independent opening and examination of the token’s referenced off-chain metadata.

## 7. Alternative explanation

A Russian businessman with a reported domestic power network provided a lavish celebration gift to friends. Separately, a pseudonymous Zora ContentCoin used wolf-themed branding. The public record does not presently supply the join key needed to merge those systems.

## 8. Defensible close

```text
TOKEN → HUMAN_NETWORK          = NOT_PROVEN
KREMLEV → COUPLE               = DOCUMENTED
IB_CHALLENGER → VENDORS        = REPORTED / SOURCE_ANCHORED
PERSONAL_FUNDS → WEDDING       = HOLD
RUSSIAN_STATE → PAYMENT_ORDER  = NOT_PROVEN
QUID_PRO_QUO                   = NOT_PROVEN
REPORT_STATUS                  = DO_NOT_FREEZE
AUTHORITY                      = FALSE
```

## Invariants

- `PATTERN != CAUSATION`
- `NATIONALITY != STATE_AFFILIATION`
- `FRIENDSHIP != QUID_PRO_QUO`
- `AFFILIATION != OWNERSHIP`
- `TOKEN_METADATA != HUMAN_IDENTITY`
- `REFERRER != CREATOR`
- `TRANSFER_PATH != CUMULATIVE_ALLOCATION`
- `HOLD != PROVEN`
- `HOLD != CLEARED`

## Sources

- [BaseScan creation transaction](https://basescan.org/tx/0x8a4bf50d040960b1a738eb243515215a1cd7611139b4ed75ac3ddffe93f981e1)
- [BaseScan token contract](https://basescan.org/address/0xe75b1EB7cdFdcE0bF0329FECEBa021DD5bE62A5C)
- [Blockscout ContentCoin implementation](https://base.blockscout.com/address/0x5DbD43785954D43c1643A0caf2ecEf9E0056Ff13)
- [ProPublica investigation](https://www.propublica.org/article/donald-trump-jr-wedding-bankrolled-russian-oligarch-umar-kremlev-putin)
- [AP confirmation report](https://apnews.com/article/donald-trump-jr-umar-kremlev-bettina-trump-wedding-russia-54b191b7d19ae09ab599ef5966523ab4)
- [Reuters congressional-inquiry report](https://www.reuters.com/world/us/us-congress-democrats-probe-russian-oligarch-financing-trump-jr-wedding-parties-2026-09-15/)
- [Project Paradise: Bettina Anderson biography](https://www.paradise.ngo/about)
- [Archived White House: Melania Trump biography](https://trumpwhitehouse.archives.gov/people/melania-trump/)
