# SCAFFOLD_NOT_YET_VERIFIED
Draft JSON-first Worker scaffold, no live attestation, no observed 200 response from Cloudflare.
The public hostname map is PROPOSED ONLY. An HTTP 200 means reachable, not byte, chain, content or authority verification.
Tests: python -m pytest -q tests/test_scaffold.py tests/test_config_anchor.py.
N52b static signature parsing is intentionally brittle and requires review on a refactor.
