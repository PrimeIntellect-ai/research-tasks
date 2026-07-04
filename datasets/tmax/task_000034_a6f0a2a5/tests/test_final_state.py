# test_final_state.py
import os
import json
import pytest

REPORT_PATH = "/home/user/policy_report.json"
SCRIPT_PATH = "/home/user/policy_check.py"

def test_policy_report_exists():
    """Verify that the policy report JSON file was created."""
    assert os.path.isfile(REPORT_PATH), f"The report file {REPORT_PATH} does not exist. Did you run your script?"

def test_policy_report_content():
    """Verify that the policy report contains the correct boolean values."""
    assert os.path.isfile(REPORT_PATH), f"Cannot check content, {REPORT_PATH} is missing."

    try:
        with open(REPORT_PATH, 'r') as f:
            report = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

    expected_keys = ["metadata_decrypted", "xss_found", "banned_function_system_found", "policy_passed"]
    for key in expected_keys:
        assert key in report, f"Key '{key}' is missing from the JSON report."
        assert isinstance(report[key], bool), f"Value for '{key}' must be a boolean."

    assert report["metadata_decrypted"] is True, "Expected 'metadata_decrypted' to be true."
    assert report["xss_found"] is True, "Expected 'xss_found' to be true, since <script> is in the metadata."
    assert report["banned_function_system_found"] is True, "Expected 'banned_function_system_found' to be true, since 'system' is used in the ELF binary."
    assert report["policy_passed"] is False, "Expected 'policy_passed' to be false, since violations were found."

def test_script_exists():
    """Verify that the student wrote the script at the requested location."""
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} is missing."