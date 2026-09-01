#!/usr/bin/env python3
"""Draft 2020-12 validator receipts for Gavel Grifter tile schema.

Fail-closed: unexpected pass on a negative fixture or fail on a positive
fixture is a validator-receipt FAIL, not a silent coercion.
"""
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "gavel-grifter-tile-v1.0.schema.json"
POS = ROOT / "fixtures" / "positive"
NEG = ROOT / "fixtures" / "negative"
OUT = ROOT / "receipts" / "validator_receipt_v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_one(validator: Draft202012Validator, path: Path) -> dict:
    instance = json.loads(path.read_text())
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    return {
        "file": path.name,
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": [
            {
                "message": e.message,
                "path": list(e.absolute_path),
                "schema_path": list(e.absolute_schema_path),
                "validator": e.validator,
            }
            for e in errors
        ],
    }


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    pos_results = [validate_one(validator, p) for p in sorted(POS.glob("*.json"))]
    neg_results = [validate_one(validator, p) for p in sorted(NEG.glob("*.json"))]

    pos_pass = all(r["valid"] for r in pos_results)
    neg_fail = all(not r["valid"] for r in neg_results)
    suite_pass = pos_pass and neg_fail and len(pos_results) > 0 and len(neg_results) > 0

    receipt = {
        "receipt_type": "SCHEMA_VALIDATOR_RECEIPT",
        "schema_id": schema.get("$id"),
        "schema_draft": schema.get("$schema"),
        "schema_path": str(SCHEMA_PATH),
        "schema_sha256": sha256(SCHEMA_PATH),
        "source_commit": "7f020457aa27c121454e4737ce3a424a54c65f8c",
        "source_repo": "jsonwisdom/CITIZEN_ROOT",
        "validator": "jsonschema.Draft202012Validator",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "wrongdoing_inference": False,
        "authority_created": False,
        "judges_scored": 0,
        "live_ingest": False,
        "positive": {
            "count": len(pos_results),
            "all_valid": pos_pass,
            "results": pos_results,
        },
        "negative": {
            "count": len(neg_results),
            "all_invalid": neg_fail,
            "results": neg_results,
        },
        "suite_status": "PASS" if suite_pass else "HOLD",
        "notes": [
            "RED != GUILT is enforced by additionalProperties:false plus wrongdoing_inference const false.",
            "system_role is required only at pipeline_stage 3 and forbidden otherwise.",
            "A public BJS hit is not PUBLICLY_REPLAYABLE unless the full checklist is true.",
            "No identity bind: fixture names are placeholders.",
        ],
    }
    OUT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({
        "suite_status": receipt["suite_status"],
        "positive_valid": pos_pass,
        "negative_invalid": neg_fail,
        "positive": [(r["file"], r["valid"]) for r in pos_results],
        "negative": [(r["file"], r["valid"], r["error_count"]) for r in neg_results],
        "receipt": str(OUT),
    }, indent=2))
    return 0 if suite_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
