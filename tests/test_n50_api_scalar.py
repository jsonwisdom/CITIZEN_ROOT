"""N50 release blocker: never expose unscoped success booleans in JSON APIs."""
import json
from pathlib import Path
import pytest
FORBIDDEN={"match","verified","ok"}
def test_n50_no_top_level_scalar_in_contract():
    p=Path("src/verify.ts")
    assert p.is_file(), "SCAFFOLD_ABSENT"
    src=p.read_text()
    # Static contract guard: runtime JSON tests required once /v1/verify exists.
    import re
    assert not re.search(r'(?<![A-Za-z0-9_])(?:match|verified|ok)\s*:',src), "D005_API_SCALAR"
def test_n50_example_json_rejects_unscoped_boolean():
    def check(payload):
        assert not (FORBIDDEN & payload.keys()), "D005_API_SCALAR"
    with pytest.raises(AssertionError,match="D005_API_SCALAR"):
        check({"match":True,"disposition":"HOLD"})
    check({"byte_integrity_only":True,"root_comparison":"MATCH","disposition":"HOLD"})
