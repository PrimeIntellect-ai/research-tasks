# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_exists():
    """Verify that the final forensics report exists at the exact required path."""
    assert os.path.isfile(REPORT_PATH), f"Forensics report not found at {REPORT_PATH}. Ensure you saved the file to the correct absolute path."

def test_report_format_and_contents():
    """Verify the JSON schema and the accuracy of the forensics findings."""
    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not a valid JSON document.")

    # Check for required keys
    required_keys = ["vulnerability_cwe", "extracted_key", "decoded_payload_user"]
    for key in required_keys:
        assert key in data, f"Missing required key '{key}' in {REPORT_PATH} JSON structure."

    # Validate CWE Identification (Allowing slight variations like CWE-22 or CWE-022)
    cwe_value = str(data["vulnerability_cwe"]).upper()
    assert "CWE-22" in cwe_value or "CWE-022" in cwe_value, \
        f"Incorrect CWE identifier. Expected a variation of CWE-22 (Path Traversal), but got: '{data['vulnerability_cwe']}'"

    # Validate Extracted Key
    expected_key = "f0r3ns1cs_k3y_9981"
    assert data["extracted_key"] == expected_key, \
        f"Incorrect extracted key. Expected '{expected_key}', but got: '{data['extracted_key']}'"

    # Validate Decoded Payload User
    expected_user = "sys_attacker"
    assert data["decoded_payload_user"] == expected_user, \
        f"Incorrect decoded payload user. Expected '{expected_user}', but got: '{data['decoded_payload_user']}'"