#!/usr/bin/env node
/**
 * CITIZEN_ROOT canonicalization.
 *
 * Rules (from CITIZEN_ROOT_INDEX verification_rules):
 *   canonicalization: UTF-8, LF, sorted object keys, no trailing whitespace
 *   hash_algorithm:   SHA-256
 *   leaf_construction: SHA-256(canonical_bytes)
 *   rewrite_forbidden: true
 *   authority: false
 *
 * Deterministic. No randomness. No authority. Fail closed.
 */

import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

function sha256Hex(data) {
  return createHash("sha256").update(data).digest("hex");
}

function stripTrailingWsLines(text) {
  const lines = text.split("\n");
  const stripped = lines.map((line) => line.replace(/[ \t\r\f\v]+$/g, ""));
  let body = stripped.join("\n");
  if (body && !body.endsWith("\n")) {
    body += "\n";
  }
  if (body.endsWith("\n\n")) {
    body = body.replace(/\n+$/, "\n");
  }
  return body;
}

export function canonicalizeText(raw) {
  let buf = Buffer.isBuffer(raw) ? raw : Buffer.from(raw, "utf8");
  if (buf.length >= 3 && buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf) {
    buf = buf.subarray(3);
  }
  let text = buf.toString("utf8");
  if (text.charCodeAt(0) === 0xfeff) {
    text = text.slice(1);
  }
  text = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  text = stripTrailingWsLines(text);
  return Buffer.from(text, "utf8");
}

function sortKeysRecursive(obj) {
  if (obj !== null && typeof obj === "object" && !Array.isArray(obj)) {
    const out = {};
    for (const k of Object.keys(obj).sort()) {
      out[k] = sortKeysRecursive(obj[k]);
    }
    return out;
  }
  if (Array.isArray(obj)) {
    return obj.map(sortKeysRecursive);
  }
  return obj;
}

export function canonicalizeJson(raw) {
  let data;
  if (typeof raw === "object" && raw !== null && !Buffer.isBuffer(raw)) {
    data = raw;
  } else {
    let buf = Buffer.isBuffer(raw) ? raw : Buffer.from(String(raw), "utf8");
    if (buf.length >= 3 && buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf) {
      buf = buf.subarray(3);
    }
    let text = buf.toString("utf8");
    if (text.charCodeAt(0) === 0xfeff) {
      text = text.slice(1);
    }
    text = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
    data = JSON.parse(text);
  }
  const ordered = sortKeysRecursive(data);
  let serialized = JSON.stringify(ordered);
  serialized = serialized.replace(/[ \t\r\n]+$/g, "") + "\n";
  return Buffer.from(serialized, "utf8");
}

function detectJson(path, raw) {
  if (path && path.toLowerCase().endsWith(".json")) return true;
  const sample = raw.toString("utf8").trimStart().slice(0, 1);
  return sample === "{" || sample === "[";
}

export function canonicalize(raw, path = null, forceJson = null) {
  const buf = Buffer.isBuffer(raw) ? raw : Buffer.from(raw);
  const useJson = forceJson !== null ? forceJson : detectJson(path, buf);
  if (useJson) {
    if (forceJson === true) {
      // Explicit JSON: fail closed, never fall back
      return canonicalizeJson(buf);
    }
    try {
      return canonicalizeJson(buf);
    } catch {
      // Auto-detect only: treat as text
      return canonicalizeText(buf);
    }
  }
  return canonicalizeText(buf);
}

export function hashCanonical(raw, path = null, forceJson = null) {
  const canonical = canonicalize(raw, path, forceJson);
  return {
    path,
    sha256: sha256Hex(canonical),
    size_bytes: canonical.length,
    canonicalization: "UTF-8, LF, sorted object keys, no trailing whitespace",
    hash_algorithm: "SHA-256",
  };
}

export function canonicalizeFile(filepath, forceJson = null) {
  const raw = readFileSync(filepath);
  const pathStr = filepath.replace(/\\/g, "/");
  const record = hashCanonical(raw, pathStr, forceJson);
  record.canonical_bytes = canonicalize(raw, pathStr, forceJson);
  return record;
}

function selfTest() {
  const failures = [];

  const rawText = Buffer.from("hello  \r\nworld\t\r\n");
  const out = canonicalizeText(rawText);
  const expected = Buffer.from("hello\nworld\n");
  if (!out.equals(expected)) {
    failures.push(`text CRLF: got ${out.toString("hex")} expected ${expected.toString("hex")}`);
  }

  const bom = Buffer.from([0xef, 0xbb, 0xbf, ...Buffer.from("alpha\n")]);
  const outBom = canonicalizeText(bom);
  if (!outBom.equals(Buffer.from("alpha\n"))) {
    failures.push(`BOM: got ${outBom}`);
  }

  const j1 = Buffer.from('{"b": 2, "a": 1}\n');
  const j2 = Buffer.from('{\n  "a": 1,\n  "b": 2\n}\n');
  const c1 = canonicalizeJson(j1);
  const c2 = canonicalizeJson(j2);
  if (!c1.equals(c2)) {
    failures.push(`JSON order: ${c1} != ${c2}`);
  }
  if (!c1.equals(Buffer.from('{"a":1,"b":2}\n'))) {
    failures.push(`JSON compact: got ${c1}`);
  }

  const nested = Buffer.from('{"z": {"b": 1, "a": 2}, "y": [3, 1]}\n');
  const cn = canonicalizeJson(nested);
  if (!cn.equals(Buffer.from('{"y":[3,1],"z":{"a":2,"b":1}}\n'))) {
    failures.push(`nested JSON: got ${cn}`);
  }

  const d1 = sha256Hex(canonicalize(Buffer.from('{"x":1,"y":2}')));
  const d2 = sha256Hex(canonicalize(Buffer.from('{"y":2,"x":1}')));
  if (d1 !== d2) failures.push("determinism failed");

  const empty = canonicalizeText(Buffer.from(""));
  if (!empty.equals(Buffer.from(""))) failures.push(`empty: got ${empty}`);

  if (failures.length) {
    for (const f of failures) console.error("FAIL:", f);
    process.exit(1);
  }

  console.log("canonicalize self-test passed");
  const sample = canonicalize(Buffer.from('{"b":2,"a":1}'));
  console.log("sample_digest:", sha256Hex(sample));
  console.log("sample_bytes:", sample.toString());
}

const isMain = process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMain) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    selfTest();
  } else if (args[0] === "-h" || args[0] === "--help") {
    console.log("Usage:");
    console.log("  node canonicalize.mjs              # self-test");
    console.log("  node canonicalize.mjs <file> [...] # print path + sha256");
    console.log("  node canonicalize.mjs --json <file>");
    console.log("  node canonicalize.mjs --text <file>");
  } else {
    let force = null;
    let files = args;
    if (args[0] === "--json") {
      force = true;
      files = args.slice(1);
    } else if (args[0] === "--text") {
      force = false;
      files = args.slice(1);
    }
    for (const fp of files) {
      const rec = canonicalizeFile(fp, force);
      console.log(JSON.stringify({
        path: rec.path,
        sha256: rec.sha256,
        size_bytes: rec.size_bytes,
      }));
    }
  }
}
