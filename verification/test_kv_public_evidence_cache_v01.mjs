import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {immutableKey, validatePinSet, readPinnedReceipt, publicResult} from "./kv_public_evidence_cache_v01.mjs";

const ROOT="85c1c9e8bf6ca6245a4c5966213508a168a25e9a766fd2798bd1f3ac44a86b7b";
const fipsList="01 02 04 05 06 08 09 10 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56".split(" ");
const sha=b=>createHash("sha256").update(b).digest("hex");
const receipt={schema:"cw-national-2026-state-build-receipt-v0.1",state_fips:"27",
  status:"GEOGRAPHY_CI_PASS_LEGAL_CAUSATION_HOLD",
  signed:false,deployed:false,legal_causation_verified:false,
  current_edges:968,county_count:87,place_count:916};
const bytes=new TextEncoder().encode(JSON.stringify(receipt)+"\n");
const hash=sha(bytes);
const pins=Object.fromEntries(fipsList.map(s=>[s,s==="27"?hash:"0".repeat(64)]));
const key=immutableKey(ROOT,"27",hash);
const kvFor=x=>({async get(requested,opts){assert.equal(requested,key);assert.equal(opts.type,"arrayBuffer");assert.equal(opts.cacheTtl,30);return x;}});
let tests=0;
const check=async(name,fn)=>{await fn();tests++;console.log("PASS",name)};
await check("exact immutable cache-key domain",()=>{
  assert.equal(key,`public-evidence/v1/sha256/${ROOT}/states/27/receipt/${hash}`);
  assert.throws(()=>immutableKey("latest","27",hash),/INVALID/);
  assert.throws(()=>immutableKey(ROOT,"../",hash),/INVALID/);
});
await check("50-state pins required",()=>{
  assert.equal(Object.keys(validatePinSet(ROOT,pins)).length,50);
  assert.throws(()=>validatePinSet(ROOT,{"27":hash}),/INCOMPLETE/);
});
await check("verified raw byte receipt PASS with no authority",async()=>{
  const r=await readPinnedReceipt(kvFor(bytes.buffer),ROOT,"27",pins);
  assert.equal(r.status,"PASS");assert.equal(r.receipt_sha256,hash);
  const p=publicResult(r);assert.equal(p.http_status,200);
  assert.equal(p.body.government_authority,false);
  assert.equal(p.body.legal_causation,"HOLD");
});
await check("missing entry fails closed (including negative cache)",async()=>{
  const r=await readPinnedReceipt(kvFor(null),ROOT,"27",pins);
  assert.deepEqual({status:r.status,reason:r.reason},{status:"HOLD",reason:"CACHE_MISS"});
  assert.equal(publicResult(r).http_status,503);
});
await check("byte tampering fails closed",async()=>{
  const tamper=new TextEncoder().encode(JSON.stringify({...receipt,current_edges:999})+"\n");
  const r=await readPinnedReceipt(kvFor(tamper.buffer),ROOT,"27",pins);
  assert.equal(r.reason,"HASH_MISMATCH");
});
await check("stale or unavailable KV must never authorize",async()=>{
  const r=await readPinnedReceipt({get(){throw Error("offline");}},ROOT,"27",pins);
  assert.equal(r.reason,"CACHE_UNAVAILABLE");
  assert.equal((await readPinnedReceipt(null,ROOT,"27",pins)).reason,"KV_NOT_BOUND");
});
await check("unknown FIPS rejected before KV read",async()=>{
  const r=await readPinnedReceipt({get(){throw Error("MUST NOT READ");}},ROOT,"03",pins);
  assert.equal(r.reason,"UNKNOWN_STATE");
});
await check("independently pinned source hash cannot be spoofed via KV metadata",async()=>{
  const wrongPins={...pins,"27":"f".repeat(64)};
  const result=await readPinnedReceipt({async get(){return bytes.buffer;}},ROOT,"27",wrongPins);
  assert.equal(result.reason,"HASH_MISMATCH");
});
await check("synthetic revoked government-authority promotion blocked",async()=>{
  const promoted={...receipt,legal_causation_verified:true};
  const altered=new TextEncoder().encode(JSON.stringify(promoted)+"\n");
  const alteredPins={...pins,"27":sha(altered)};
  const result=await readPinnedReceipt({async get(){return altered.buffer;}},ROOT,"27",alteredPins);
  assert.equal(result.reason,"CONTENT_GUARD_INVALID");
});
console.log("CW_KV_PROTOTYPE_CI_PASS tests="+tests+" deploy=false namespace_created=false bindings_modified=false");
