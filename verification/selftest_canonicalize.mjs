#!/usr/bin/env node
/**
 * CITIZEN_ROOT canonicalization self-test (Node).
 *
 * Fail closed. Machine-readable result on stdout.
 * Primary assertion: canonical bytes == unhex(expected_canonical_hex).
 * Secondary assertion: SHA-256.
 * Cross-language: Node bytes == Python bytes == expected bytes.
 */
import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { canonicalize } from "./canonicalize.mjs";

const PROTOCOL = "CITIZEN_ROOT_INDEX_V0_1";
const __dirname = dirname(fileURLToPath(import.meta.url));
const VECTOR_DIR = join(__dirname, "test_vectors");
const VECTOR_FILES = ["basic.json", "whitespace.json", "unicode.json", "nested.json"];

function sha256Hex(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

function loadVectors() {
  const vectors = [];
  for (const name of VECTOR_FILES) {
    const path = join(VECTOR_DIR, name);
    if (!existsSync(path)) {
      throw new Error(`missing vector suite: ${path}`);
    }
    const doc = JSON.parse(readFileSync(path, "utf8"));
    for (const vectorId of doc.vectors) {
      const recordPath = join(VECTOR_DIR, "vectors", `${vectorId}.json`);
      const v = JSON.parse(readFileSync(recordPath, "utf8"));
      v._suite = name;
      v._raw = readFileSync(join(VECTOR_DIR, v.input_file));
      v._expectedBytes = Buffer.from(v.expected_canonical_hex, "hex");
      vectors.push(v);
    }
  }
  return vectors;
}

function runNode(v) {
  const forceJson = v.format === "json";
  const got = canonicalize(v._raw, null, forceJson);
  return { bytes: got, sha256: sha256Hex(got) };
}

function runPython(v) {
  const force = v.format === "json" ? "json" : "text";
  const py = spawnSync("python3", ["-c", `
import sys, json, base64
sys.path.insert(0, ${JSON.stringify(__dirname)})
from canonicalize import canonicalize, sha256_hex
raw = sys.stdin.buffer.read()
force = sys.argv[1] == "json"
got = canonicalize(raw, path=None, force_json=force)
print(json.dumps({"bytes_b64": base64.b64encode(got).decode(), "sha256": sha256_hex(got)}))
`, force], {
    cwd: __dirname,
    input: v._raw,
    encoding: "buffer",
  });
  if (py.status !== 0) {
    throw new Error(`python failed for ${v.id}: ${(py.stderr || Buffer.alloc(0)).toString()}`);
  }
  const payload = JSON.parse(py.stdout.toString("utf8"));
  return {
    bytes: Buffer.from(payload.bytes_b64, "base64"),
    sha256: payload.sha256,
  };
}

function pythonAvailable() {
  const r = spawnSync("python3", ["--version"], { encoding: "utf8" });
  return r.status === 0;
}

const result = {
  protocol: PROTOCOL,
  python_node_equivalence: null,
  vectors_passed: 0,
  vectors_failed: 0,
  status: "FAIL",
  failures: [],
  suites: VECTOR_FILES,
};

let vectors;
try {
  vectors = loadVectors();
} catch (e) {
  result.failures.push({ id: "_load", error: String(e) });
  result.vectors_failed = 1;
  console.log(JSON.stringify(result, null, 2));
  process.exit(1);
}

const pyOk = pythonAvailable();
let equivalenceChecked = 0;
let equivalenceOk = true;

for (const v of vectors) {
  const expectedBytes = v._expectedBytes;
  const expectedHash = v.expected_sha256;
  let got;
  try {
    got = runNode(v);
  } catch (e) {
    result.vectors_failed += 1;
    result.failures.push({ id: v.id, suite: v._suite, error: `node exception: ${e}` });
    continue;
  }

  if (!got.bytes.equals(expectedBytes)) {
    result.vectors_failed += 1;
    result.failures.push({
      id: v.id,
      suite: v._suite,
      error: "node canonical bytes mismatch (primary)",
      expected_canonical_hex: expectedBytes.toString("hex"),
      got_canonical_hex: got.bytes.toString("hex"),
    });
    continue;
  }
  if (got.sha256 !== expectedHash) {
    result.vectors_failed += 1;
    result.failures.push({
      id: v.id,
      suite: v._suite,
      error: "node sha256 mismatch (secondary)",
      expected_sha256: expectedHash,
      got_sha256: got.sha256,
    });
    continue;
  }

  if (pyOk) {
    try {
      const py = runPython(v);
      equivalenceChecked += 1;
      if (!py.bytes.equals(got.bytes) || py.sha256 !== got.sha256) {
        equivalenceOk = false;
        result.vectors_failed += 1;
        result.failures.push({
          id: v.id,
          suite: v._suite,
          error: "python_node_bytes_mismatch",
          python_sha256: py.sha256,
          node_sha256: got.sha256,
        });
        continue;
      }
    } catch (e) {
      equivalenceOk = false;
      result.vectors_failed += 1;
      result.failures.push({ id: v.id, suite: v._suite, error: `python exception: ${e}` });
      continue;
    }
  }

  result.vectors_passed += 1;
}

if (pyOk) {
  result.python_node_equivalence =
    equivalenceOk &&
    equivalenceChecked === result.vectors_passed &&
    result.vectors_failed === 0;
} else {
  result.python_node_equivalence = null;
}

result.status = result.vectors_failed === 0 ? "PASS" : "FAIL";
console.log(JSON.stringify(result, null, 2));
process.exit(result.status === "PASS" ? 0 : 1);
