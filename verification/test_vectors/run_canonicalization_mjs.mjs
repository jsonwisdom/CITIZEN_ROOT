#!/usr/bin/env node
/** Run frozen vectors against canonicalize.mjs.

Primary assertion: canonical bytes == unhex(expected_canonical_hex).
Secondary assertion: SHA-256.
*/
import { readFileSync, readdirSync } from "node:fs";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { canonicalize } from "../canonicalize.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const VECTORS_DIR = __dirname;
const VECTOR_JSON_DIR = join(VECTORS_DIR, "vectors");

function sha256Hex(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

const vectorFiles = readdirSync(VECTOR_JSON_DIR)
  .filter((name) => name.endsWith(".json"))
  .sort();

let failed = 0;

for (const name of vectorFiles) {
  const v = JSON.parse(readFileSync(join(VECTOR_JSON_DIR, name), "utf8"));
  const raw = readFileSync(join(VECTORS_DIR, v.input_file));
  const forceJson = v.format === "json";
  const got = canonicalize(raw, null, forceJson);
  const expected = Buffer.from(v.expected_canonical_hex, "hex");
  const gotHash = sha256Hex(got);
  if (!got.equals(expected)) {
    console.log(`FAIL bytes ${v.id}`);
    console.log(`  expected: ${expected.toString("hex")}`);
    console.log(`  got:      ${got.toString("hex")}`);
    failed += 1;
    continue;
  }
  if (gotHash !== v.expected_sha256) {
    console.log(`FAIL hash  ${v.id}: ${gotHash} != ${v.expected_sha256}`);
    failed += 1;
    continue;
  }
  console.log(`PASS ${v.id}`);
}

if (failed) {
  console.log(`\n${failed} failure(s)`);
  process.exit(1);
}
console.log(`\n${vectorFiles.length} vectors passed (Node bytes + SHA-256)`);
