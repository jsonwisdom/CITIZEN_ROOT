# Deterministic Idea Machine

`machine_id: IMA-0001`  
`authority_pointer: jaywisdom.base.eth`  
`repository_authority: false`  
`status: INITIALIZED`

The Deterministic Idea Machine converts preserved conceptual inputs into reproducible, structured idea packets. It does not create truth, ownership, identity, or authority.

## Axioms

1. Preserve the exact input before interpretation.
2. Canonicalize and hash every machine-readable input.
3. Apply transformations in an explicitly versioned order.
4. Treat ambiguity as a branch; never silently correct it.
5. Use deterministic tie-breakers. Randomness is forbidden in canonical mode.
6. Record rejected branches and the rule that rejected them.
7. Separate user-asserted authority from machine and audit authority.
8. Every output references its input digests, ruleset digest, and execution receipt.

## Input space

An input packet contains:

- exact source material or stable source pointers;
- explicit constraints and desired output class;
- optional prior concepts, vocabularies, and ontologies;
- an ordered ruleset identifier;
- an optional integer seed used only by a fully specified deterministic algorithm.

Missing required fields produce a gap receipt, not an inferred value.

## Transformation logic

`PRESERVE → CANONICALIZE → HASH → VALIDATE → EXPAND BRANCHES → APPLY ORDERED RULES → FILTER → RANK → EMIT → RECEIPT`

- Expansion rules must name their finite candidate space.
- Filters execute in declared order.
- Ranking uses declared integer or exact-rational scores.
- Ties resolve by canonical UTF-8 byte order unless the ruleset declares another deterministic method.
- Replaying identical canonical inputs under the same ruleset and runtime contract must produce the same semantic output.

## Output space

The machine emits an idea packet containing:

- structured ideas;
- provenance pointers;
- applied and rejected transformations;
- unresolved gaps;
- deterministic ordering;
- input, ruleset, output, and receipt digests.

Supported initial output classes are structured concepts, visual-layout specifications, documentation maps, and code-architecture plans.

## Constraints

- No stochastic drift in canonical mode.
- No silent normalization or correction.
- No evidence duplication in CITIZEN_ROOT; pointers and digests only.
- No mutation of sealed inputs or historical receipts.
- No authority, identity, species, ownership, or truth created by hashing.
- No external execution, publication, merge, or deployment without explicit authorization.

## Initial gate

`IMA-GAP-0001 = OPEN`

The machine is initialized, but the first domain-specific ruleset, input packet, and expected output schema have not yet been selected.

