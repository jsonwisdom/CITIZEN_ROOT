"""N52b static checks are scaffold-specific, NOT proof of independent anchoring.
A TypeScript refactor may require updating the signature parser; that is not
automatically an anchor regression. Missing scaffold is SKIP here only; the
separate test_scaffold_present MUST hard fail.
"""
from pathlib import Path
import re
import pytest
WRANGLER, SRC = Path("wrangler.toml"), Path("src/verify.ts")
pytestmark = pytest.mark.skipif(
    not (WRANGLER.is_file() and SRC.is_file()),
    reason="scaffold absent — anchor untestable, see test_scaffold_present",
)
def test_n52b_no_mutable_anchor_constant():
    assert not re.search(r'TRUSTED_MANIFEST_BASE\s*=\s*["\x27][^"\x27]+["\x27]', WRANGLER.read_text()), "N52b: config-defined trust root"
def test_n52b_verify_explicit_anchor_scope():
    """Specific to function verify(...) syntax: refactors require human review."""
    m = re.search(r'\bfunction\s+verify\s*\(([^)]*)\)', SRC.read_text(), re.S)
    assert m is not None, "signature parser no longer matches; review test"
    assert re.search(r'\banchor\b', m.group(1)), "explicit anchor parameter missing"
