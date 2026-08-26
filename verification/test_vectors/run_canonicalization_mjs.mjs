#!/usr/bin/env node
/**
 * Run frozen vectors against canonicalize.mjs.
 *
 * Primary assertion: canonical bytes == unhex(expected_canonical_hex)
 * Secondary assertion: SHA-256(canonical bytes) == expected_sha256
 */
import { readFileSync, readdirSync } from "node:fs";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { canonicalize } from "../canonicalize.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const VECTORS_DIR = __dirname;

function sha256Hex(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

function loadVectors() {
  const dir = join(VECTORS_DIR, "vectors");
  return readdirSync(dir)
    .filter((name) => name.endsWith(".json"))
    .sort()
    .map((name) => {
      const path = join(dir, name);
      return JSON.parse(readFileSync(path, "utf8"));
    });
}

const vectors = loadVectors();
let failed = 0;

for (const v of vectors) {
  const raw = readFileSync(join(VECTORS_DIR, v.input_file));
  const forceJson = v.format === "json";
  const got = canonicalize(raw, null, forceJson);
  const expected = Buffer.from(v.expected_canonical_hex, "hex");
  if (!got.equals(expected)) {
    console.log(`FAIL bytes ${v.id}`);
    console.log(`  expected_hex: ${expected.toString("hex")}`);
    console.log(`  got_hex:      ${got.toString("hex")}`);
    failed++;
    continue;
  }
  const gotHash = sha256Hex(got);
  if (gotHash !== v.expected_sha256) {
    console.log(`FAIL hash  ${v.id}: ${gotHash} != ${v.expected_sha256}`);
    failed++;
    continue;
  }
  console.log(`PASS ${v.id}`);
}

if (failed) {
  console.log(`\n${failed} failure(s)`);
  process.exit(1);
}
console.log(`\n${vectors.length} vectors passed (Node)`);
