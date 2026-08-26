# verification

Canonicalization, hashing, Merkle construction, and replay helpers.

## Rules (from CITIZEN_ROOT_INDEX)

- **canonicalization**: UTF-8, LF, sorted object keys, no trailing whitespace
- **hash_algorithm**: SHA-256
- **leaf_construction**: SHA-256(canonical_bytes)
- **merkle_construction**: ordered binary tree by path
- **rewrite_forbidden**: true
- **authority**: false

## Merkle implementation

Two equivalent, deterministic implementations:

| File | Language |
|------|----------|
| `merkle.py` | Python 3 |
| `merkle.mjs` | Node.js (ESM) |

### Construction rules

1. Collect leaves as `{path, sha256}` where `sha256` is already the digest of the canonical bytes of the artifact.
2. Sort leaves strictly by `path` (lexicographic).
3. Build levels bottom-up by pairing consecutive hashes:
   - parent = SHA-256( left_raw_32_bytes + right_raw_32_bytes )
4. When a level has an odd number of nodes, the final unpaired node is **promoted** (not duplicated).
5. The single remaining hash is the Merkle root.

### Usage (Python)

```python
from merkle import build_merkle_tree, generate_inclusion_proof, verify_inclusion

leaves = [
    {"path": "AL/AGENT_WISDOM.md", "sha256": "..."},
    {"path": "JOY/leaves.sha256", "sha256": "..."},
]

tree = build_merkle_tree(leaves)
print(tree["root"])

proof = generate_inclusion_proof(leaves, "AL/AGENT_WISDOM.md")
assert verify_inclusion(proof["leaf_sha256"], proof["proof"], proof["root"])
```

### Usage (Node)

```js
import { buildMerkleTree, generateInclusionProof, verifyInclusion } from "./merkle.mjs";

const leaves = [
  { path: "AL/AGENT_WISDOM.md", sha256: "..." },
  { path: "JOY/leaves.sha256", sha256: "..." },
];

const tree = buildMerkleTree(leaves);
console.log(tree.root);

const proof = generateInclusionProof(leaves, "AL/AGENT_WISDOM.md");
console.assert(verifyInclusion(proof.leaf_sha256, proof.proof, proof.root));
```

### Self-test

```bash
python3 merkle.py
node merkle.mjs
```

Both must print a deterministic tree and "self-test passed".

## Invariants

- Same ordered set of (path, sha256) pairs always produces the identical root.
- Inclusion proofs are compact and independently verifiable.
- No central authority is required to recompute or check a proof.
