# test_final_state.py

import os
import json
import pytest

def test_audit_report_exists():
    path = "/home/user/audit_report.json"
    assert os.path.isfile(path), f"Expected audit report not found at {path}"

def test_audit_report_content():
    path = "/home/user/audit_report.json"
    assert os.path.isfile(path), f"Expected audit report not found at {path}"

    with open(path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {path} as JSON: {e}")

    assert "issuer_id" in report, "Missing 'issuer_id' in audit report"
    assert report["issuer_id"] == "SEC_8832_XYZ", f"Incorrect issuer_id: expected 'SEC_8832_XYZ', got {report['issuer_id']}"

    assert "chain_valid" in report, "Missing 'chain_valid' in audit report"
    assert report["chain_valid"] is True, f"Incorrect chain_valid: expected True, got {report['chain_valid']}"

    assert "vulnerable_tokens" in report, "Missing 'vulnerable_tokens' in audit report"
    expected_tokens = ["token2.jwt", "token3.jwt"]
    actual_tokens = report["vulnerable_tokens"]

    assert isinstance(actual_tokens, list), f"'vulnerable_tokens' should be a list, got {type(actual_tokens)}"
    assert sorted(actual_tokens) == expected_tokens, f"Incorrect vulnerable_tokens: expected {expected_tokens}, got {actual_tokens}"