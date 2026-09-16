# NIGHT WOLFE MONEY RAIL — CHAIN-STATE V0.2

**Snapshot:** 2026-09-16  
**Chain:** Base  
**Posture:** WATCH_ONLY_CHAIN  
**Authority:** false  
**Promotion:** none  
**Source boundary:** Transaction values in this artifact were supplied with the chain-state update. Public web search returned no indexed result for the new contract or transaction at snapshot time; independent RPC/explorer replay remains pending.

> Object identifier: `NIGHT_WOLFE_MONEY_RAIL_V0_2`  
> On-chain token name: `NIGHT WOLF 💒`

## 1. Creation receipt

- Creation transaction: `0x8a4bf50d040960b1a738eb243515215a1cd7611139b4ed75ac3ddffe93f981e1`
- Block: `51394203`
- Reported timestamp: `2026-09-16T16:55:53Z`
- Reported status: `SUCCESS`
- Execution path: Account-abstraction bundle via Coinbase Bundler and EntryPoint v0.6.0
- Creation-receipt gap: `RESOLVED_AS_SUPPLIED`
- Independent replay: `PENDING`

## 2. Contract rail

- Address: `0xe75b1EB7cdFdcE0bF0329FECEBa021DD5bE62A5C`
- Class: `ZORA_CONTENT_COIN` / minimal proxy
- Implementation: `0x5DbD43785954D43c1643A0caf2ecEf9E0056Ff13`
- Name: `NIGHT WOLF 💒`
- Symbol: `NIGHTJR`
- Factory: `0x777777751622c0d3258f214F9DF38E35BF45baF3`
- Creation method: factory call inside an AA UserOperation
- Creator/factory caller: `HOLD` — bundler mediation does not establish ultimate origin at this layer

## 3. Supply rail

- Total supply: `1,000,000,000 NIGHTJR`
- Reported atomic transfer path:
  1. `10,000,000 NIGHTJR` to `0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2`
  2. `990,000,000 NIGHTJR` to intermediate `0x0469a4Bd3724DC86C9542F4694c976DA13C450c0`
  3. Approximately `989,999,999.999… NIGHTJR` from the intermediate path toward Uniswap V4 Pool Manager `0x498581fF718922c3f8e6A244956aF099B2652b2b`

The second and third entries describe a path through the same bulk supply, not cumulative independent allocations.

Token overview pages reportedly showed zero holders and zero transfers at snapshot time. This conflicts with the supplied transaction-level transfer observations and remains classified as `INDEXER_CONFLICT`.

## 4. Liquidity rail

- Pool initialized: `TRUE_AS_SUPPLIED`
- Pool Manager: `0x498581fF718922c3f8e6A244956aF099B2652b2b`
- First transfers: `VISIBLE_IN_CREATION_TX_AS_SUPPLIED`
- Subsequent external trades: `HOLD`
- Market activity: `HOLD`

`POOL_MANAGER_RECEIPT != EXTERNAL_MARKET_ACTIVITY`

## 5. Referrer rail

- Address: `0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2`
- Reported token receipt: `10,000,000 NIGHTJR`
- Reported same-transaction ZORA movement: approximately `10.07 ZORA`
- Role: `FEE_ROUTING / INITIAL_ALLOCATION / METADATA_ONLY`
- Authority effect: none

`REFERRER_METADATA != CREATOR_IDENTITY`  
`TOKEN_RECEIPT != FACTORY_CALLER`  
`SAME_TX_FLOW != CAUSAL_OWNERSHIP`

## 6. Ledger object

```json
{
  "object_id": "NIGHT_WOLFE_MONEY_RAIL_V0_2",
  "snapshot": "2026-09-16",
  "chain": "BASE",
  "authority": false,
  "posture": "WATCH_ONLY_CHAIN",
  "verification_boundary": {
    "receipt_values": "USER_SUPPLIED",
    "independent_chain_replay": "PENDING",
    "web_index_result": "ABSENT_AT_SNAPSHOT"
  },
  "contract": {
    "address": "0xe75b1EB7cdFdcE0bF0329FECEBa021DD5bE62A5C",
    "class": "ZORA_CONTENT_COIN",
    "implementation": "0x5DbD43785954D43c1643A0caf2ecEf9E0056Ff13",
    "factory": "0x777777751622c0d3258f214F9DF38E35BF45baF3",
    "name": "NIGHT WOLF 💒",
    "symbol": "NIGHTJR",
    "creation_tx": "0x8a4bf50d040960b1a738eb243515215a1cd7611139b4ed75ac3ddffe93f981e1",
    "creation_block": 51394203,
    "creation_receipt": "RESOLVED_AS_SUPPLIED",
    "creator_or_factory_caller": "HOLD"
  },
  "supply": {
    "total_supply": "1000000000",
    "transfer_path": [
      {
        "to": "0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2",
        "amount": "10000000"
      },
      {
        "to": "0x0469a4Bd3724DC86C9542F4694c976DA13C450c0",
        "amount": "990000000"
      },
      {
        "from_path": "0x0469a4Bd3724DC86C9542F4694c976DA13C450c0",
        "to": "0x498581fF718922c3f8e6A244956aF099B2652b2b",
        "amount": "~989999999.999..."
      }
    ],
    "token_page_holders": 0,
    "token_page_transfers": 0,
    "state": "INDEXER_CONFLICT"
  },
  "liquidity": {
    "pool_initialized": "TRUE_AS_SUPPLIED",
    "pool_manager": "0x498581fF718922c3f8e6A244956aF099B2652b2b",
    "first_transfer": "VISIBLE_IN_CREATION_TX_AS_SUPPLIED",
    "external_market_activity": "HOLD"
  },
  "referrer": {
    "address": "0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2",
    "token_receipt": "10000000",
    "same_tx_zora_movement": "~10.07",
    "role": "FEE_ROUTING_INITIAL_ALLOCATION_METADATA_ONLY"
  },
  "critical_missing_receipt": null,
  "next_open_receipt": "ULTIMATE_AA_ORIGIN_AND_FACTORY_CALLER"
}
```

## 7. Invariants

- `EXPLORER_SHOWS_ZERO != ONCHAIN_ZERO`
- `TOTAL_SUPPLY_OBSERVED + ZERO_TRANSFERS_ON_TOKEN_PAGE = INDEXER_CONFLICT`
- `TRANSFER_PATH != CUMULATIVE_DISTRIBUTION`
- `POOL_INITIALIZATION != EXTERNAL_TRADE`
- `REFERRER != CREATOR_IDENTITY`
- `HOLD != PROVEN`
- `HOLD != CLEARED`

## 8. Posture lock

```text
POSTURE             = WATCH_ONLY_CHAIN
AUTHORITY           = FALSE
CREATION_RECEIPT    = RESOLVED_AS_SUPPLIED
INDEPENDENT_REPLAY  = PENDING
MARKET_ACTIVITY     = HOLD
ULTIMATE_AA_ORIGIN  = HOLD
```

No money-flow claim extends beyond the supplied atomic creation transaction. No provenance is promoted beyond what that transaction is reported to record.

## Navigation

- [BaseScan transaction](https://basescan.org/tx/0x8a4bf50d040960b1a738eb243515215a1cd7611139b4ed75ac3ddffe93f981e1)
- [BaseScan contract](https://basescan.org/address/0xe75b1EB7cdFdcE0bF0329FECEBa021DD5bE62A5C)
