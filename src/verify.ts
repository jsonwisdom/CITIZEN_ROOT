/** SCAFFOLD_NOT_YET_VERIFIED. JSON-only status API: 200 means reachability, not verification. */
type Anchor = {id:string; provenance:"CALLER_SUPPLIED"|"EXTERNALLY_ATTESTED"|"UNRESOLVED"};
export function verify(anchor: Anchor | null) {
  return {byte_integrity:"UNKNOWN",chain_integrity:"UNKNOWN",historical_authorized:"UNKNOWN",
    current_authorized:"UNKNOWN",content_verified:"UNKNOWN",authority_established:"UNKNOWN",
    observer_provenance:"UNKNOWN",time_provenance:"UNKNOWN",manifest_root:null,claimed_root:null,
    spec:"manifest/1 · event/0 · v0.8-draft",anchor:anchor?.id??null,
    anchor_provenance:anchor?.provenance??"UNRESOLVED",negs:["003"],
    warns:["SCAFFOLD_ONLY","NO_BYTES_HASHED","NOT_A_VERIFIER"],
    verifier_build:"UNBUILT",policy:"NON_NORMATIVE_DRAFT",scaffold_status:"SCAFFOLD_NOT_YET_VERIFIED"};
}
export default {async fetch(request:Request):Promise<Response>{
  const url = new URL(request.url), allowed=["/","/health","/v0/status","/v0/ideas"];
  const found=request.method==="GET"&&allowed.includes(url.pathname);
  const verdict=verify(null);
  const body=found?(url.pathname==="/v0/ideas"?{...verdict,
    concept:"Random ideas → structured JSON evidence → independent replay → review → DNS reachability",
    math:{domain_hash:"SHA256(UTF8(domain)||0x00||JCS(without_root))",
      uniform_collision_model:"2^-256 (assumption, not evidence of trust)"},
    proposed_hosts:["verify.jsonwisdom.com","jason.jsonwisdom.com","ledger.jsonwisdom.com",
      "receipts.jsonwisdom.com","librarian.jsonwisdom.com","staging.jsonwisdom.com"]}:verdict):
      {error:"NOT_IMPLEMENTED",disposition:"HOLD",scaffold_status:"SCAFFOLD_NOT_YET_VERIFIED"};
  return new Response(JSON.stringify(body,null,2),{status:found?200:404,
    headers:{"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"}});
}};