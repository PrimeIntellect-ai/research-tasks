# test_final_state.py
import os
import json
import base64
import pytest

def compute_expected_pin() -> str:
    """
    Recomputes the expected PIN by bruteforcing the custom hashing algorithm
    to match the known target hash (0x1337cfeb) from the binary.
    """
    target_hash = 0x1337cfeb
    for i in range(10000):
        pin = f"{i:04d}"
        h = 0x1337BEEF
        for char in pin:
            # Simulate 32-bit unsigned integer operations
            h = ((h << 4) ^ (h >> 28) ^ ord(char)) & 0xFFFFFFFF
        if h == target_hash:
            return pin
    pytest.fail("Test setup error: Could not compute expected PIN.")

@pytest.fixture(scope="session")
def expected_data():
    pin = compute_expected_pin()
    payload = f"{pin}:DUMP_AUDIT"
    payload_base64 = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    return {
        "pin": pin,
        "payload_base64": payload_base64,
        "valid_cwes": {"CWE-798", "CWE-259"}
    }

def test_audit_trail_log_created():
    log_path = "/home/user/audit_trail.log"
    assert os.path.exists(log_path), (
        f"The audit log {log_path} was not created. "
        "Ensure you successfully executed the legacy_processor binary with the correct base64 payload."
    )

    with open(log_path, "r") as f:
        content = f.read()

    expected_msg = "AUDIT_SUCCESS: COMPLIANCE_DATA_EXTRACTED"
    assert expected_msg in content, (
        f"The audit log {log_path} exists but does not contain the expected success message. "
        f"Expected to find '{expected_msg}'."
    )

def test_compliance_audit_json(expected_data):
    json_path = "/home/user/compliance_audit.json"
    assert os.path.exists(json_path), f"The final report file {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"The file {json_path} does not contain valid JSON. Error: {e}")

    # Validate PIN
    assert "pin" in data, f"The JSON file {json_path} is missing the 'pin' key."
    assert data["pin"] == expected_data["pin"], (
        f"The submitted PIN is incorrect. "
        f"Expected the 4-digit string that hashes to 0x1337cfeb."
    )

    # Validate Base64 Payload
    assert "payload_base64" in data, f"The JSON file {json_path} is missing the 'payload_base64' key."
    assert data["payload_base64"] == expected_data["payload_base64"], (
        f"The submitted base64 payload is incorrect. "
        f"Ensure it is exactly the base64 encoding of '[PIN]:DUMP_AUDIT'."
    )

    # Validate CWE ID
    assert "cwe_id" in data, f"The JSON file {json_path} is missing the 'cwe_id' key."
    assert data["cwe_id"] in expected_data["valid_cwes"], (
        f"The submitted CWE ID '{data['cwe_id']}' is incorrect. "
        f"Expected the standard CWE identifier for 'Use of Hard-coded Credentials' (e.g., CWE-798)."
    )