import hashlib, urllib.request, urllib.error, pytest
PIN="1d9cecc376b41a2da8f0083c370dfc55ca9070c6"
BASE="https://raw.githubusercontent.com/jsonwisdom/CITIZEN_ROOT/{}/docs/jason-clock/MANIFEST_V1_CANDIDATE.json"
# The GitHub API must be used for authenticated/private repos.
# An unauthenticated 404 is INACCESSIBLE, not proof of absence.
def fetch(ref):
    req=urllib.request.Request(BASE.format(ref),headers={"User-Agent":"jason-verifier-draft"})
    with urllib.request.urlopen(req,timeout=15) as response: return response.read()
def test_n52a_pin_snapshot():
    # Baseline must be independently committed by review; never generate it
    # automatically on first run.
    from pathlib import Path
    expected=Path("tests/snapshots/pinned_manifest.sha256")
    if not expected.exists(): pytest.skip("BASELINE_NOT_ESTABLISHED")
    try: body=fetch(PIN)
    except urllib.error.HTTPError as e: pytest.skip(f"PIN_FETCH_INACCESSIBLE_{e.code}")
    assert hashlib.sha256(body).hexdigest()==expected.read_text().split()[0]
def test_n52a_main_measurement():
    try: a=hashlib.sha256(fetch(PIN)).hexdigest(); b=hashlib.sha256(fetch("main")).hexdigest()
    except urllib.error.HTTPError as e: pytest.skip(f"REF_FETCH_INACCESSIBLE_{e.code}")
    print({"main_equals_pin":a==b,"pinned_sha256":a,"main_sha256":b})
