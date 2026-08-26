#!/usr/bin/env node
/** Run frozen canonicalization vectors against canonicalize.mjs. Byte-level equality. */
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { canonicalize } from "../canonicalize.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const VECTORS = join(__dirname, "canonicalization.json");

function sha256Hex(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

const doc = JSON.parse(readFileSync(VECTORS, "utf8"));
const vectors = doc.vectors;
let failed = 0;

for (const v of vectors) {
  const raw = Buffer.from(v.input, "utf8");
  const forceJson = v.format === "json" ? true : false;
  const got = canonicalize(raw, null, forceJson);
  const expected = Buffer.from(v.expected_canonical, "utf8");
  const gotHash = sha256Hex(got);
  if (!got.equals(expected)) {
    console.log(`FAIL bytes ${v.id}`);
    console.log(`  expected: ${JSON.stringify(expected.toString("utf8"))}`);
    console.log(`  got:      ${JSON.stringify(got.toString("utf8"))}`);
    failed++;
    continue;
  }
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
