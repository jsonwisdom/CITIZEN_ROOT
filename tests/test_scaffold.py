"""Missing scaffold is a hard failure, never a skip."""
from pathlib import Path
REQUIRED = (Path("src/verify.ts"), Path("wrangler.toml"))
def test_scaffold_present():
    absent = [str(p) for p in REQUIRED if not p.is_file()]
    assert not absent, "SCAFFOLD_ABSENT: " + ", ".join(absent)
def test_scaffold_self_describes_unverified_state():
    assert all(p.is_file() for p in REQUIRED), "SCAFFOLD_ABSENT: cannot read status marker"
    sources = (*REQUIRED, Path("SCAFFOLD_STATUS.md"))
    assert any(p.is_file() and "SCAFFOLD_NOT_YET_VERIFIED" in p.read_text() for p in sources), "SELF_DESCRIPTION_MISSING"
