import pathlib, re
import pytest
# N52b is a RED test by design: intended to identify future unsafe config.
WRANGLER = pathlib.Path("wrangler.toml")
SRC = pathlib.Path("src/verify.ts")
def test_n52b_no_mutable_anchor_literal():
    if not WRANGLER.exists():
        pytest.fail("SCAFFOLD_NOT_PRESENT: wrangler.toml")
    config=WRANGLER.read_text()
    assert not re.search(r'TRUSTED_MANIFEST_BASE\s*=\s*"[^"]+"',config), "DRAFT_ANCHOR_CONFIG_MUTABLE"
def test_n52b_anchor_explicitly_scoped():
    if not SRC.exists():
        pytest.fail("SCAFFOLD_NOT_PRESENT: src/verify.ts")
    src=SRC.read_text()
    assert "anchor" in src, "ANCHOR_SCOPE_MISSING"
# This static test cannot demonstrate anchor independence. Only an external
# trust-root witness and adversarial mutation test can do that.
