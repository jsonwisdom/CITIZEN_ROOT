# JASON Clock Membrane — manifest/1 candidate (NON-NORMATIVE)

`manifest/1` binds to `jason.manifest.v1.hash`. The root is `SHA256(UTF8(domain) || 0x00 || JCS(manifest excluding root))`, lower-case hex.

Historical `manifest/0` draft roots MUST be retained with their distinct domain tags; their ambiguity is explicitly recorded, not silently normalized. Root is not a signature, independent evidence, or chain position.

Closed fetch status set remains unchanged. Run defects `D001`–`D004` void the run; do not record those as REJECT. Do not conflate time provenance with processing timestamp.

No DNS or Worker mutation; no production release; no signed leaf; no supersession event appended to an anchored chain.

Run locally: `python3 verify_manifest.py docs/jason-clock/MANIFEST_V1_CANDIDATE.json` (script below).
