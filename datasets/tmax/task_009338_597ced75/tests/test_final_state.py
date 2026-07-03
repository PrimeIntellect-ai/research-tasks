# test_final_state.py

import os
import json
import pytest

def test_policy_report_exists():
    """Test that the policy_report.json file was created."""
    filepath = "/home/user/policy_report.json"
    assert os.path.isfile(filepath), f"File {filepath} does not exist. The Rust program must generate this file."

def test_policy_report_content():
    """Test that the policy_report.json contains the correct boolean results."""
    filepath = "/home/user/policy_report.json"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    try:
        with open(filepath, 'r') as f:
            report = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {filepath} does not contain valid JSON.")

    expected_keys = {"open_redirect_found", "cert_valid", "integrity_valid"}
    assert set(report.keys()) == expected_keys, f"Report keys {set(report.keys())} do not match expected keys {expected_keys}."

    assert report["open_redirect_found"] is True, "Expected 'open_redirect_found' to be true."
    assert report["cert_valid"] is True, "Expected 'cert_valid' to be true."
    assert report["integrity_valid"] is False, "Expected 'integrity_valid' to be false."