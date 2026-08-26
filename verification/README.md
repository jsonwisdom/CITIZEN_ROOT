# verification

Canonicalization, hashing, Merkle construction, and replay helpers.

## Rules (from CITIZEN_ROOT_INDEX)

- **canonicalization**: UTF-8, LF, sorted object keys, no trailing whitespace
- **hash_algorithm**: SHA-256
- **leaf_construction**: SHA-256(canonical_bytes)
- **merkle_construction**: ordered binary tree by path
- **rewrite_forbidden**: true
- **authority**: false

## Canonicalization

Two equivalent, deterministic implementations:

| File | Language |
|------|----------|
| `canonicalize.py` | Python 3 |
| `canonicalize.mjs` | Node.js (ESM) |

### Text rules

1. Decode as UTF-8 (strict). Strip BOM if present.
2. Normalize all line endings to LF (`\r\n` / `\r` → `\n`).
3. Strip trailing whitespace on every line.
4. Non-empty result ends with exactly one LF.
5. Empty input stays empty.

### JSON rules

1. Parse JSON.
2. Recursively sort object keys (array order preserved).
3. Serialize compact: `separators=(',', ':')`, `ensure_ascii=False`.
4. Single trailing LF. No trailing whitespace.

### Usage (Python)

```python
from canonicalize import canonicalize, hash_canonical, canonicalize_file

raw = open("artifact.json", "rb").read()
canonical = canonicalize(raw, path="artifact.json")
record = hash_canonical(raw, path="artifact.json")
print(record["sha256"])
```

```bash
python3 canonicalize.py                          # self-test
python3 canonicalize.py path/to/file.json        # print path + sha256
python3 canonicalize.py --json path/to/file
python3 canonicalize.py --text path/to/file.md
```

### Usage (Node)

```js
import { canonicalize, hashCanonical, canonicalizeFile } from "./canonicalize.mjs";

const raw = fs.readFileSync("artifact.json");
const canonical = canonicalize(raw, "artifact.json");
const record = hashCanonical(raw, "artifact.json");
console.log(record.sha256);
```

```bash
node canonicalize.mjs                            # self-test
node canonicalize.mjs path/to/file.json
node canonicalize.mjs --json path/to/file
node canonicalize.mjs --text path/to/file.md
```

### Cross-implementation invariant

Both implementations must produce the identical digest for the same input.
Self-test sample (`{"b":2,"a":1}` → `{"a":1,"b":2}\n`):

```
e8d38819d39f705646bfb643368eca78f7db476c16471dbc33b941b27326410d
```

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
assert verify_inclusion(proof["path"], proof["leaf_sha256"], proof["proof"], proof["root"])
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
console.assert(verifyInclusion(proof.path, proof.leaf_sha256, proof.proof, proof.root));
```

### Self-test

```bash
python3 merkle.py
node merkle.mjs
python3 canonicalize.py
node canonicalize.mjs
```

All four must print deterministic output and "self-test passed".

## Pipeline

```
artifact bytes
      ↓
canonicalize (UTF-8, LF, sorted keys, no trailing ws)
      ↓
SHA-256 → leaf digest
      ↓
ordered Merkle tree (by path)
      ↓
root + inclusion proofs
```

## Invariants

- Same ordered set of (path, sha256) pairs always produces the identical root.
- Inclusion proofs are compact and independently verifiable.
- Canonicalization is pure: same bytes in → same bytes out, across Python and Node.
- No central authority is required to recompute or check a proof.
