# NIGHT WOLFE — ABI ROLE DECODE V0.1

**Object ID:** `NIGHT_WOLFE_ABI_ROLE_DECODE_V0_1`  
**Snapshot:** 2026-09-16 UTC  
**Scope:** Creation transaction only  
**Status:** `ROLE_DECODE_COMPLETE_WITH_BOUNDARIES`  
**Authority:** `false`

## Target

- Contract: `0xe75b1EB7cdFdcE0bF0329FECEBa021DD5bE62A5C`
- Creation transaction: `0x8a4bf50d040960b1a738eb243515215a1cd7611139b4ed75ac3ddffe93f981e1`
- Block: `51394203`
- No later-block market search was performed.

## Nested call path

1. Outer transaction sender / bundler beneficiary: `0x8D47bA07Ff9ccCCF58c7E8810eE42c0Dc8B8b123`.
2. EntryPoint v0.6.0: `0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789`.
3. `handleOps` selector: `0x1fad948c`.
4. UserOperation sender: `0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2`.
5. CoinbaseSmartWallet `executeBatch((address,uint256,bytes)[])` selector: `0x34fcd5be`.
6. Batch target: ZoraFactory `0x777777751622c0d3258f214F9DF38E35BF45baF3`, value `0`.
7. Factory `deployWithHook(address,address[],string,string,string,bytes,address,address,bytes)` selector: `0x0d36fc77`.

## Decoded creation roles

| Role | Address / state | Receipt |
|---|---|---|
| UserOperation sender | `0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2` | EntryPoint `UserOperationEvent`, log 160 |
| Factory caller | `0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2` | `CoinCreatedV4.caller`, log 157 |
| Payout recipient | `0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2` | calldata, `CoinCreatedV4`, and `payoutRecipient()` at creation block |
| Token owners | `0x829AdfEd…`, `0xB3b9Cc…`, `0xD88a5B…` | calldata and `owners()` at creation block |
| Platform referrer | `0x7D009Ad14339e5Ab6fbd107978f429fBc5669961` | calldata, `CoinCreatedV4`, and `platformReferrer()` |
| Currency | `0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F` | poolConfig, `CoinCreatedV4`, and `currency()`; Blockscout identifies a CreatorCoin proxy |
| Trade referrer | `NOT_PRESENT_IN_CREATION_CALL` | Not a `deployWithHook` parameter; no creation-transaction `Swap` |
| Deploy hook | zero address | calldata |
| Deploy hook data | empty bytes | calldata |
| PoolKey hook | `0x0469a4Bd3724DC86C9542F4694c976DA13C450c0` | `CoinCreatedV4.poolKey.hooks`; distinct from the zero-valued deploy hook |
| ERC-4337 paymaster | `0x2FAEB0760D4230Ef2aC21496Bb4F0b47D634FD4c` | `UserOperationEvent` |
| Bundler / beneficiary | `0x8D47bA07Ff9ccCCF58c7E8810eE42c0Dc8B8b123` | outer transaction and `handleOps.beneficiary`; not the creator |

## Factory payload

- Payout recipient: `0x829AdfEd…`.
- Owners: three addresses — `0x829AdfEd…`, `0xB3b9Cc…`, and `0xD88a5B…`.
- URI: `ipfs://bafybeicl6qa75lb7swjwavni3eo4ilaoqxe4xtdphyya6dd6qmvhwry23y`.
- Name: `NIGHT WOLF 💒`.
- Symbol: `NIGHTJR`.
- Platform referrer: `0x7D009Ad…`.
- Currency: `0x694cE46C…`.
- Deploy hook: zero address.
- Hook data: empty.

## Classification boundary

`0x829AdfEd…` is now decoded as the smart-wallet UserOperation sender, factory caller, payout recipient, one token owner, and 10M-token recipient. This resolves address-level protocol roles. It does **not** prove the natural person controlling the wallet, the signer used for this UserOperation, or a relationship to any person in the human-network hypothesis.

The three token-owner addresses are contract-level owners of the ContentCoin. They must not be conflated with CoinbaseSmartWallet signers or natural-person identity.

A trade referrer is supplied during trading activity, not by this creation call. `PLATFORM_REFERRER != TRADE_REFERRER`.

## Updated state vector

```text
CREATION_TX_REPLAY     = COMPLETE
SUPPLY_TRACE           = COMPLETE
POOL_INITIALIZATION    = CONFIRMED
CREATION_TX_SWAP       = NONE_OBSERVED
ABI_ROLE_DECODE        = COMPLETE
USEROP_SENDER          = 0x829AdfEd...
FACTORY_CALLER         = 0x829AdfEd...
PAYOUT_RECIPIENT       = 0x829AdfEd...
PLATFORM_REFERRER      = 0x7D009Ad...
CURRENCY               = 0x694cE46C...
TRADE_REFERRER         = NOT_PRESENT_IN_CREATION_CALL
ULTIMATE_AA_ORIGIN     = HOLD
OFFCHAIN_METADATA      = HOLD
LATER_MARKET_ACTIVITY  = HOLD
HUMAN_NETWORK_JOIN     = NOT_PROVEN
REPORT_STATUS          = DO_NOT_FREEZE
AUTHORITY              = FALSE
```

## Invariants

- `BUNDLER != CREATOR`
- `USEROP_SENDER != NATURAL_PERSON_IDENTITY`
- `FACTORY_CALLER != ULTIMATE_AA_ORIGIN`
- `PAYOUT_RECIPIENT != HUMAN_IDENTITY`
- `TOKEN_OWNER != SMART_WALLET_SIGNER`
- `PLATFORM_REFERRER != TRADE_REFERRER`
- `POOLKEY_HOOK != DEPLOY_HOOK`
- `CREATION_ROLE_DECODE != LATER_MARKET_SEARCH`
- `HOLD != PROVEN`
- `HOLD != CLEARED`
- `AUTHORITY = FALSE`

## Sources

- [BaseScan creation transaction](https://basescan.org/tx/0x8a4bf50d040960b1a738eb243515215a1cd7611139b4ed75ac3ddffe93f981e1)
- [Blockscout transaction](https://base.blockscout.com/tx/0x8a4bf50d040960b1a738eb243515215a1cd7611139b4ed75ac3ddffe93f981e1)
- [Blockscout ZoraFactory implementation](https://base.blockscout.com/address/0xbbAe128a65239c3328fAa0c70B8D5F9C961a8038)
- [Blockscout ContentCoin implementation](https://base.blockscout.com/address/0x5DbD43785954D43c1643A0caf2ecEf9E0056Ff13)
- [Blockscout Zora V4 coin hook](https://base.blockscout.com/address/0x0469a4Bd3724DC86C9542F4694c976DA13C450c0)
