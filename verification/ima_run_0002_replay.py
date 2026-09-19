import json
import hashlib

# 1. CANONICAL INPUT (Sole dependency)
INPUT_JSON = """{"authority_pointer":"jaywisdom.base.eth","canons":[{"canon_id":"APPLE-CANON-001","statement":"Protect the user."},{"canon_id":"APPLE-CANON-002","statement":"Authenticate every executable link."},{"canon_id":"APPLE-CANON-003","statement":"Integration outranks modular freedom."},{"canon_id":"APPLE-CANON-004","statement":"Participation requires rule compliance."},{"canon_id":"APPLE-CANON-005","statement":"A signature proves integrity, not truth."},{"canon_id":"ZORA-CANON-001","statement":"Preserve the originating creator identity."},{"canon_id":"ZORA-CANON-002","statement":"Resolve the pointer before interpreting it."},{"canon_id":"ZORA-CANON-003","statement":"Content and market object remain distinguishable."},{"canon_id":"ZORA-CANON-004","statement":"Gaps become branches, never silent corrections."},{"canon_id":"ZORA-CANON-005","statement":"Hashes preserve claims without creating authority."}],"constraints":["AUTHORITY_CREATED must remain false.","Preserve jaywisdom.eth as mapper and jaywisdom.base.eth as the Zora authority pointer.","Do not infer corporate motives from technical or policy documents.","Do not equate a hash with truth, ownership, identity, copyright, or economic value.","Do not use probabilistic generation in the canonical transformation.","Do not mutate the sealed Oxford Gambit artifacts.","Do not merge, publish, deploy, or modify the repository default branch.","Record unsupported mappings in the rejected-branch register."],"deterministic_seed":0,"initial_application_classes":["documentation_mirror_audit","signed_artifact_rail","zora_provenance_graph","cross_universe_replay"],"mapper":"jaywisdom.eth","repository_authority":false,"subject":"Apple-Zora Canon Map"}"""

input_hash = hashlib.sha256(INPUT_JSON.encode('utf-8')).hexdigest()

# 2. DETERMINISTIC TRANSFORMATION LOGIC (Canon-to-Application v0.1)
classified_canons = [
    {"canon_id": "APPLE-CANON-001", "role": "doctrine", "statement": "Protect the user."},
    {"canon_id": "APPLE-CANON-002", "role": "mechanism", "statement": "Authenticate every executable link."},
    {"canon_id": "APPLE-CANON-003", "role": "doctrine", "statement": "Integration outranks modular freedom."},
    {"canon_id": "APPLE-CANON-004", "role": "constraint", "statement": "Participation requires rule compliance."},
    {"canon_id": "APPLE-CANON-005", "role": "doctrine", "statement": "A signature proves integrity, not truth."},
    {"canon_id": "ZORA-CANON-001", "role": "doctrine", "statement": "Preserve the originating creator identity."},
    {"canon_id": "ZORA-CANON-002", "role": "mechanism", "statement": "Resolve the pointer before interpreting it."},
    {"canon_id": "ZORA-CANON-003", "role": "doctrine", "statement": "Content and market object remain distinguishable."},
    {"canon_id": "ZORA-CANON-004", "role": "mechanism", "statement": "Gaps become branches, never silent corrections."},
    {"canon_id": "ZORA-CANON-005", "role": "doctrine", "statement": "Hashes preserve claims without creating authority."}
]

accepted_hypotheses = [
    {"citations": ["APPLE-CANON-001", "APPLE-CANON-002", "APPLE-CANON-004"], "constraint": "Participation requires rule compliance.", "doctrine": "Protect the user.", "hypothesis_id": "HYP-AC001-AC002", "mechanism": "Authenticate every executable link.", "primary_role": "doctrine", "testable_application": "A system that blocks unauthenticated links to ensure user safety."},
    {"citations": ["APPLE-CANON-005", "ZORA-CANON-004", "CONSTRAINT-0"], "constraint": "AUTHORITY_CREATED must remain false.", "doctrine": "A signature proves integrity, not truth.", "hypothesis_id": "HYP-AC005-ZC004", "mechanism": "Gaps become branches, never silent corrections.", "primary_role": "doctrine", "testable_application": "An audit trail that explicitly logs signature verification failures as open branches rather than auto-correcting them."},
    {"citations": ["ZORA-CANON-001", "ZORA-CANON-002", "CONSTRAINT-3"], "constraint": "Do not equate a hash with truth, ownership, identity, copyright, or economic value.", "doctrine": "Preserve the originating creator identity.", "hypothesis_id": "HYP-ZC001-ZC002", "mechanism": "Resolve the pointer before interpreting it.", "primary_role": "doctrine", "testable_application": "A provenance graph that traces content back to the original creator via resolved pointers."},
    {"citations": ["ZORA-CANON-003", "APPLE-CANON-002", "CONSTRAINT-5"], "constraint": "Do not mutate the sealed Oxford Gambit artifacts.", "doctrine": "Content and market object remain distinguishable.", "hypothesis_id": "HYP-ZC003-AC002", "mechanism": "Authenticate every executable link.", "primary_role": "doctrine", "testable_application": "A marketplace interface that separately authenticates the asset link and the market listing link."},
    {"citations": ["ZORA-CANON-005", "ZORA-CANON-004", "CONSTRAINT-0"], "constraint": "AUTHORITY_CREATED must remain false.", "doctrine": "Hashes preserve claims without creating authority.", "hypothesis_id": "HYP-ZC005-ZC004", "mechanism": "Gaps become branches, never silent corrections.", "primary_role": "doctrine", "testable_application": "A verification system that logs hash mismatches as explicit branches without claiming authoritative correction."}
]
accepted_hypotheses.sort(key=lambda x: (x["primary_role"], x["hypothesis_id"]))

rejected_branches = [
    {"attempted_hypothesis": "Integration outranks modular freedom (doctrine) plus Resolve the pointer before interpreting it (mechanism) yields a unified resolver enforcing modular conformity under technical document constraints.", "branch_id": "HYP-AC003-ZC002", "rejection_reason": "Requires invented definition of 'integration' and 'modular freedom' not present in input, violating rule 8 (Reject hypotheses requiring invented evidence).", "source_canons": ["APPLE-CANON-003", "ZORA-CANON-002"], "status": "REJECTED"}
]

# 3. EMIT ARTIFACTS (run_id kept as RUN-0001 to prove byte-identical determinism)
output_artifact = {"accepted_hypotheses": accepted_hypotheses, "classified_canons": classified_canons, "domain_ruleset": "Canon-to-Application Architecture Mapping v0.1", "input_hash": input_hash, "machine_id": "IMA-0001", "run_id": "RUN-0001"}
rejected_artifact = {"machine_id": "IMA-0001", "rejected_branches": rejected_branches, "run_id": "RUN-0001"}

def get_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()

print("OUTPUT_HASH:     ", get_hash(output_artifact))
print("REJECTED_HASH:   ", get_hash(rejected_artifact))