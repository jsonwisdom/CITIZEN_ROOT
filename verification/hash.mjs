#!/usr/bin/env node
/** Thin SHA-256 helper. Leaf construction = SHA-256(canonical_bytes). */
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

export function sha256(data) {
  return createHash("sha256").update(data).digest();
}

export function sha256Hex(data) {
  return createHash("sha256").update(data).digest("hex");
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const buf = process.argv[2]
    ? readFileSync(process.argv[2])
    : readFileSync(0);
  process.stdout.write(sha256Hex(buf) + "\n");
}
