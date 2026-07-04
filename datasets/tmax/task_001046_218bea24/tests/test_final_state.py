# test_final_state.py
import json
import os
import hashlib
import pytest

REPORT_PATH = '/home/user/policy_report.json'
CRITICAL_FILE_PATH = '/home/user/system/critical_config.txt'
EXPECTED_PRE_HASH = '839446d1fa7a47d2c3e1b72e90f209df3db0fba4bf1f02194944d18080f4f9f1'

def test_report_exists_and_valid_json():
    """Verify that the policy report exists and is valid JSON."""
    assert os.path.isfile(REPORT_PATH), f"Report file missing at {REPORT_PATH}"
    try:
        with open(REPORT_PATH, 'r') as f:
            json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

def test_report_contents():
    """Verify the contents of the generated JSON report."""
    assert os.path.isfile(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    assert 'auth_missing_status' in data, "Key 'auth_missing_status' is missing in the report."
    assert data['auth_missing_status'] == 401, f"Expected auth_missing_status to be 401, got {data['auth_missing_status']}"

    assert 'auth_provided_status' in data, "Key 'auth_provided_status' is missing in the report."
    assert data['auth_provided_status'] == 200, f"Expected auth_provided_status to be 200, got {data['auth_provided_status']}"

    assert 'pre_attack_hash' in data, "Key 'pre_attack_hash' is missing in the report."
    assert data['pre_attack_hash'] == EXPECTED_PRE_HASH, f"Expected pre_attack_hash to be {EXPECTED_PRE_HASH}, got {data['pre_attack_hash']}"

    assert 'post_attack_hash' in data, "Key 'post_attack_hash' is missing in the report."
    assert data['post_attack_hash'] != data['pre_attack_hash'], "Expected post_attack_hash to differ from pre_attack_hash, but they are identical."

    assert 'is_vulnerable' in data, "Key 'is_vulnerable' is missing in the report."
    assert data['is_vulnerable'] is True, f"Expected is_vulnerable to be True, got {data['is_vulnerable']}"

def test_critical_file_overwritten():
    """Verify that the critical config file was actually overwritten by the exploit."""
    assert os.path.isfile(CRITICAL_FILE_PATH), f"Critical file missing at {CRITICAL_FILE_PATH}"

    with open(CRITICAL_FILE_PATH, 'r') as f:
        content = f.read().strip()

    assert content == "PWNED", f"Expected the critical file content to be 'PWNED', but got '{content}'"