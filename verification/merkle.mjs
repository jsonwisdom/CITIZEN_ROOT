#!/usr/bin/env node
/**
 * CITIZEN_ROOT ordered binary Merkle tree construction.
 *
 * Rules (from CITIZEN_ROOT_INDEX verification_rules):
 *   - hash_algorithm: SHA-256
 *   - leaf_construction: SHA-256(canonical_bytes)
 *   - merkle_construction: ordered binary tree by path
 *   - rewrite_forbidden: true
 *   - authority: false
 *
 * Deterministic. No randomness. No authority.
 */

import { createHash } from "crypto";

function sha256Hex(data) {
  return createHash("sha256").update(data).digest("hex");
}

function pairHash(leftHex, rightHex) {
  const left = Buffer.from(leftHex, "hex");
  const right = Buffer.from(rightHex, "hex");
  return sha256Hex(Buffer.concat([left, right]));
}

/**
 * Build an ordered binary Merkle tree.
 *
 * @param {Array<{path: string, sha256: string}>} leaves
 * @returns {object}
 */
export function buildMerkleTree(leaves) {
  if (!leaves || leaves.length === 0) {
    return {
      algorithm: "SHA-256",
      construction: "ordered binary tree by path",
      leaf_count: 0,
      root: null,
      levels: [],
      leaves: [],
    };
  }

  const sortedLeaves = [...leaves].sort((a, b) =>
    a.path < b.path ? -1 : a.path > b.path ? 1 : 0
  );

  let current = sortedLeaves.map((l) => l.sha256);
  const levels = [current.slice()];

  while (current.length > 1) {
    const nextLevel = [];
    for (let i = 0; i < current.length; i += 2) {
      if (i + 1 < current.length) {
        nextLevel.push(pairHash(current[i], current[i + 1]));
      } else {
        // Promote the unpaired node
        nextLevel.push(current[i]);
      }
    }
    current = nextLevel;
    levels.push(current.slice());
  }

  return {
    algorithm: "SHA-256",
    construction: "ordered binary tree by path",
    leaf_count: sortedLeaves.length,
    root: current[0] ?? null,
    levels,
    leaves: sortedLeaves.map((l) => ({ path: l.path, sha256: l.sha256 })),
  };
}

/**
 * Verify a Merkle inclusion proof.
 */
export function verifyInclusion(leafSha256, proof, root) {
  let current = leafSha256;
  for (const step of proof) {
    if (step.side === "left") {
      current = pairHash(step.hash, current);
    } else if (step.side === "right") {
      current = pairHash(current, step.hash);
    } else {
      return false;
    }
  }
  return current === root;
}

/**
 * Generate an inclusion proof for a given path.
 */
export function generateInclusionProof(leaves, targetPath) {
  const tree = buildMerkleTree(leaves);
  if (tree.root === null) return null;

  const idx = tree.leaves.findIndex((l) => l.path === targetPath);
  if (idx === -1) return null;

  const proof = [];
  let currentIdx = idx;

  for (let li = 0; li < tree.levels.length - 1; li++) {
    const level = tree.levels[li];
    if (currentIdx % 2 === 0) {
      if (currentIdx + 1 < level.length) {
        proof.push({ side: "right", hash: level[currentIdx + 1] });
      }
    } else {
      proof.push({ side: "left", hash: level[currentIdx - 1] });
    }
    currentIdx = Math.floor(currentIdx / 2);
  }

  return {
    path: targetPath,
    leaf_sha256: tree.leaves[idx].sha256,
    proof,
    root: tree.root,
  };
}

// Self-test when run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const sample = [
    { path: "b.txt", sha256: sha256Hex("content-b") },
    { path: "a.txt", sha256: sha256Hex("content-a") },
    { path: "c.txt", sha256: sha256Hex("content-c") },
  ];
  const tree = buildMerkleTree(sample);
  console.log(JSON.stringify(tree, null, 2));

  const proof = generateInclusionProof(sample, "a.txt");
  const ok = verifyInclusion(proof.leaf_sha256, proof.proof, proof.root);
  console.log("self-test", ok ? "passed" : "FAILED");
  process.exit(ok ? 0 : 1);
}
