// COMPUTER WISDOM — KV public-evidence cache design v0.1; NOT DEPLOYED.
// A content-addressed read-through interface: no mutable 'latest' pointer,
// no authorization decision, no writes, no secrets, no automatic promotion.
// Readers accept a cache entry only when its raw bytes match the SHA-256
// committed in the verified original-state receipt index.
const HEX64 = /^[0-9a-f]{64}$/;
const FIPS = /^[0-9]{2}$/;
const decoder = new TextDecoder("utf-8", {fatal: true});
const encoder = new TextEncoder();

export function immutableKey(root, fips, receiptSha) {
  if (!HEX64.test(root) || !FIPS.test(fips) || !HEX64.test(receiptSha)) {
    throw new Error("INVALID_IMMUTABLE_CACHE_KEY");
  }
  return `public-evidence/v1/sha256/${root}/states/${fips}/receipt/${receiptSha}`;
}

export function validatePinSet(root, hashes) {
  if (!HEX64.test(root) || !hashes || typeof hashes !== "object" || Array.isArray(hashes)) {
    throw new Error("PIN_SET_INVALID");
  }
  const keys = Object.keys(hashes);
  if (keys.length !== 50 || new Set(keys).size !== 50 ||
      keys.some(k => !FIPS.test(k) || !HEX64.test(hashes[k]))) {
    throw new Error("PIN_SET_INCOMPLETE");
  }
  return Object.freeze({...hashes});
}

const toHex = buffer => Array.from(new Uint8Array(buffer), n => n.toString(16).padStart(2, "0")).join("");

export async function readPinnedReceipt(kv, root, state, hashes) {
  // The caller provides a build-pinned 50-state hash index, not KV-supplied
  // metadata. A stale KV entry cannot introduce a new authorized hash.
  const pins = validatePinSet(root, hashes);
  if (!FIPS.test(state) || !Object.hasOwn(pins, state)) {
    return {status:"HOLD", reason:"UNKNOWN_STATE", receipt:null};
  }
  if (!kv || typeof kv.get !== "function") {
    return {status:"HOLD", reason:"KV_NOT_BOUND", receipt:null};
  }
  const hash = pins[state];
  const key = immutableKey(root, state, hash);
  let value;
  try {
    value = await kv.get(key, {type:"arrayBuffer", cacheTtl:30});
  } catch {
    return {status:"HOLD", reason:"CACHE_UNAVAILABLE", receipt:null};
  }
  if (value === null || value === undefined) {
    return {status:"HOLD", reason:"CACHE_MISS", receipt:null};
  }
  const bytes = value instanceof ArrayBuffer ? value :
                ArrayBuffer.isView(value) ? value.buffer.slice(value.byteOffset,value.byteOffset + value.byteLength) : null;
  if (!bytes) return {status:"HOLD", reason:"CACHE_TYPE_INVALID", receipt:null};
  const actual = toHex(await crypto.subtle.digest("SHA-256", bytes));
  if (actual !== hash) {
    return {status:"HOLD", reason:"HASH_MISMATCH", receipt:null};
  }
  let receipt;
  try {
    receipt = JSON.parse(decoder.decode(bytes));
  } catch {
    return {status:"HOLD", reason:"INVALID_JSON", receipt:null};
  }
  if (receipt?.state_fips !== state ||
      receipt?.schema !== "cw-national-2026-state-build-receipt-v0.1" ||
      receipt?.status !== "GEOGRAPHY_CI_PASS_LEGAL_CAUSATION_HOLD" ||
      receipt?.legal_causation_verified !== false ||
      receipt?.signed !== false ||
      receipt?.deployed !== false) {
    return {status:"HOLD", reason:"CONTENT_GUARD_INVALID", receipt:null};
  }
  return {status:"PASS", source:"PINNED_IMMUTABLE_KV_CACHE", root,
          state_fips:state, receipt_sha256:hash, receipt};
}

export function publicResult(result) {
  if (result.status !== "PASS") {
    return {http_status:503, body:{status:"HOLD",reason:result.reason,
      verified:false,government_authority:false,legal_causation:"HOLD"}};
  }
  return {http_status:200, body:{status:"PASS",root:result.root,
    state_fips:result.state_fips,sha256:result.receipt_sha256,
    receipt:result.receipt,verified:true,government_authority:false,
    legal_causation:"HOLD"}};
}

// No KV.put, KV.delete, cloudflare.request or remote fetch is invoked here.
// No live worker imports this file; it is prototype-only.
