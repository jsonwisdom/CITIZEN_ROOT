# ZeroDayTodayJay — Gold Book / Market / Accord Supplement — 2026-09-17

Status: APPEND_ONLY_SUPPLEMENT
Authority: false
Parent: `ZERODAYTODAYJAY_TREASURY_RESET_CLAIM_REPLAY_2026-09-17.md`
Mode: PUBLIC_RECORD_REPLAY / NO_FAKE_GREEN

## 1. Adversarial mirror: corporation / collateral claims

The mirror claim set is retained as an adversarial test, not promoted as fact.

### 28 U.S.C. § 3002(15)
The phrase “United States means … a Federal corporation” appears inside **Title 28, Part VI, Chapter 176 — Federal Debt Collection Procedure**, and the section expressly says the definitions apply “as used in this chapter.” It does not say that the Constitution was replaced by a private corporation or that citizens became corporate collateral.

Primary source: https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid%3AUSC-prelim-title28-section3002

### District of Columbia Organic Act of 1871
The 1871 Act created a municipal government for the **District of Columbia**. Historical statutory compilations describe the District as successor to the former Washington and Georgetown corporations. That is not an incorporation of the United States as a private company.

Primary sources:
- https://www.govinfo.gov/content/pkg/STATUTE-16/pdf/STATUTE-16-Pg419.pdf
- https://www.govinfo.gov/content/pkg/STATUTE-18/pdf/STATUTE-18-Pg1.pdf

### Federal Reserve ownership
The Federal Reserve System remains a statutory central-bank system with a federal Board of Governors, the FOMC, and 12 separately incorporated Reserve Banks. Member banks hold required Reserve Bank stock, but the Federal Reserve states that this stock does not carry the ordinary control or financial interest of private-company common stock and cannot be sold or pledged.

Primary sources:
- https://www.federalreserve.gov/faqs/about_14986.htm
- https://www.federalreserve.gov/faqs/about_12593.htm
- https://www.federalreserve.gov/frrs/statutes/section-5-stock-issues-increase-and-decrease-of-capital.htm

### Fourteenth Amendment
Section 1 establishes U.S. and state citizenship for persons born or naturalized in the United States and subject to its jurisdiction. The amendment does not create a citizen-as-surety or citizen-as-collateral rule.

Primary source: https://www.archives.gov/founding-docs/amendments-11-27

Disposition:

```text
USA_PRIVATE_CORPORATION_FROM_1871 = REJECT_AS_STATED
28_USC_3002_GLOBAL_CORPORATE_ADMISSION = REJECT_AS_STATED
FED_PRIVATE_SHAREHOLDER_CARTEL = REJECT_AS_STATED
14A_CITIZEN_AS_DEBT_SURETY = REJECT_AS_STATED
```

## 2. Gold Reserve Act of 1934: what actually moved

The Gold Reserve Act of 1934 was approved January 30, 1934. Section 2 transferred to the United States all right, title, interest, and claims of the Federal Reserve Board, Federal Reserve Banks, and Federal Reserve agents in gold coin and bullion. In payment, equivalent dollar credits were established in Treasury accounts, payable in gold certificates.

Primary source: https://fraser.stlouisfed.org/title/gold-reserve-act-1934-1085/fulltext

The Act did **not** abolish the Federal Reserve System. It changed gold title, redemption, reserve plumbing, and created the statutory foundation for the Exchange Stabilization Fund.

On January 31, 1934, Proclamation 2072 changed the gold content of the dollar; Treasury’s contemporaneous release stated a $35-per-fine-ounce purchase price under the new regime. Treasury’s ESF history states that Congress appropriated $2 billion to the ESF from the increment created by reducing the weight of the gold dollar.

Primary sources:
- https://www.presidency.ucsb.edu/documents/white-house-statement-proclamation-2072
- https://home.treasury.gov/policy-issues/international/exchange-stabilization-fund/legislative-basis

Order-of-magnitude replay using 194 million fine ounces:

```text
194,000,000 × ($35.00 - $20.67) ≈ $2.78 billion
```

This is a historical-method illustration, not a claim that the exact Treasury close was determined by this rounded input.

```text
1934_REVALUATION = STATUTE + TITLE_SHIFT + PROCLAMATION + BOOK_GAIN
FED_REPLACED_1934 = FALSE
```

## 3. Treasury–Federal Reserve Accord of 1951

During World War II, the Fed formally committed to a 3/8 percent peg on short-term Treasury bills, while long-term Treasury yields were also held down under wartime financing policy. The dispute over continued support intensified during the Korean War inflation period.

On March 4, 1951, Treasury and the Federal Reserve announced that they had reached accord on debt-management and monetary policies, including the objective of minimizing monetization of the public debt. Federal Reserve historical materials describe the agreement as separating government debt management from monetary policy and ending the standing wartime rate-control regime after a transition.

Primary source: https://www.federalreservehistory.org/essays/treasury-fed-accord

The Accord was not a Gold Reserve Act amendment, not a gold revaluation, and not a replacement of the Federal Reserve Act.

```text
1951_ACCORD = PEG_EXIT + MONETARY_POLICY_SPACE + TRANSITION
FED_REPLACED_1951 = FALSE
GOLD_REVALUED_1951 = FALSE
```

## 4. Gold accounting: same ounces, different valuation methods

### Method 1 — statutory book value
31 U.S.C. § 5117 fixes the gold-certificate valuation at **$42 and two-ninths per fine troy ounce**. Treasury’s gold report describes its book value as $42.2222 per fine troy ounce.

Primary sources:
- https://uscode.house.gov/view.xhtml?edition=2023&num=0&req=granuleid%3AUSC-2023-title31-section5117
- https://fiscal.treasury.gov/resources/gold-report

A Treasury gold report lists approximately **261.499 million fine troy ounces** and approximately **$11.041 billion** of statutory book value.

### Method 2 — date-stamped market value
Treasury OIG separately reports market value for the Federal Reserve Bank-held portion of U.S. gold. At September 30, 2025, the OIG schedule showed **13.4528 million fine troy ounces**, **$568.0 million statutory value**, and **$51.461 billion market value** using the LBMA Gold Price PM of **$3,825.30**.

Primary source: https://oig.treasury.gov/system/files/2026-01/OIG-26-004-%28secured%2C-508%29.pdf

### Method 3 — gold certificates
Gold certificates are dollar claims issued against Treasury gold under § 5117 and are bounded by the statutory valuation. They are not a second pile of physical gold and are not a public redemption right at market price.

```text
SAME_OUNCES + STATUTORY_RATE = BOOK_VALUE
SAME_OUNCES + NAMED_MARKET_PRICE = INDICATIVE_MARKET_VALUE
GOLD_CERTIFICATES <= STATUTORY_VALUE_OF_GOLD_HELD_AGAINST_THEM
BOOK_VALUE != MARKET_VALUE
MARKET_VALUE != AUTOMATIC_TREASURY_SPENDABLE_CASH
```

## 5. 2026 reset-claim membrane

A modern statutory revaluation would require a new legal/administrative action changing the operative gold accounting or certificate framework and specifying the resulting treatment. A higher spot price alone does not change the § 5117 book rate.

```text
GOLD_DRIVEN_HIGH_FOR_DEBT_RESET = HOLD / NO_RECEIPT
2026_SPOT_GAP = MARKET_VALUATION_DELTA
2026_SPOT_GAP != 1934_REVALUATION_EVENT
FED_SECRETLY_REPLACED = REJECT_AS_STATED
AUTHORITY_CREATED = FALSE
```

## 6. Private Finances membrane

Personal financial data remains outside this public packet. Finances was consulted only to preserve the private/public boundary. No account balance, transaction, holding, account identifier, or financial-memory object is copied into this GitHub/Drive supplement.

```text
PERSONAL_RAIL_3 = OFF_TABLE
PRIVATE_FINANCES -> PUBLIC_GITHUB = BLOCKED
PRIVATE_FINANCES -> PUBLIC_DRIVE = BLOCKED
FINANCIAL_MEMORY_WRITE = NONE
```

## Replay close

```text
APPEND_ONLY = TRUE
FACTS_PROMOTED_FROM_ADVERSARIAL_MIRROR = 0
CROSS_SURFACE_BYTE_IDENTITY = HOLD
CANON_UPGRADE = FALSE
AUTHORITY_CREATED = FALSE
```
