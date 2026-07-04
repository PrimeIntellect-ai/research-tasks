# test_final_state.py

import os
import json
import hashlib
import pytest

REPORT_PATH = "/home/user/audit_report.json"
AUTH_KEYS_PATH = "/home/user/.ssh/authorized_keys"
COMPROMISED_PATH = "/home/user/compromised.txt"

@pytest.fixture
def report_data():
    """Reads and parses the JSON report, ensuring it exists and is valid."""
    assert os.path.isfile(REPORT_PATH), f"The report file {REPORT_PATH} was not found. Did the Rust program generate it?"

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON. Error: {e}")

    return data

def test_report_structure(report_data):
    """Verifies that all required keys are present in the JSON report."""
    expected_keys = {"compromised_keys", "open_port", "decoded_response", "response_hash"}
    actual_keys = set(report_data.keys())
    missing_keys = expected_keys - actual_keys

    assert not missing_keys, f"The JSON report is missing the following required keys: {missing_keys}"

def test_compromised_keys(report_data):
    """Derives the expected compromised keys from the system state and verifies the report."""
    assert os.path.isfile(AUTH_KEYS_PATH), f"Missing setup file {AUTH_KEYS_PATH}"
    assert os.path.isfile(COMPROMISED_PATH), f"Missing setup file {COMPROMISED_PATH}"

    # Read the known compromised hashes
    with open(COMPROMISED_PATH, "r", encoding="utf-8") as f:
        compromised_hashes = set(line.strip() for line in f if line.strip())

    expected_compromised = []

    # Parse authorized_keys and hash the base64 data to find matches
    with open(AUTH_KEYS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                b64_data = parts[1]
                # Compute SHA256 of the base64 string as UTF-8 bytes
                computed_hash = hashlib.sha256(b64_data.encode("utf-8")).hexdigest()
                if computed_hash in compromised_hashes:
                    expected_compromised.append(computed_hash)

    actual_compromised = report_data.get("compromised_keys")
    assert isinstance(actual_compromised, list), "The 'compromised_keys' value in the report must be a JSON array (list)."

    assert sorted(actual_compromised) == sorted(expected_compromised), \
        f"The reported compromised keys do not match the expected values.\nExpected: {expected_compromised}\nActual: {actual_compromised}"

def test_open_port(report_data):
    """Verifies that the correct open port was identified."""
    actual_port = report_data.get("open_port")
    assert actual_port == 8005, f"Expected 'open_port' to be 8005, but got {actual_port}."

def test_decoded_response(report_data):
    """Verifies the decoded response string from the service."""
    expected_response = "FLAG_7b_vulnerable_service_found_7d"
    actual_response = report_data.get("decoded_response")

    assert actual_response == expected_response, \
        f"Expected 'decoded_response' to be '{expected_response}', but got '{actual_response}'."

def test_response_hash(report_data):
    """Verifies the SHA256 hash of the decoded response."""
    expected_response = "FLAG_7b_vulnerable_service_found_7d"
    expected_hash = hashlib.sha256(expected_response.encode("utf-8")).hexdigest()
    actual_hash = report_data.get("response_hash")

    assert actual_hash == expected_hash, \
        f"Expected 'response_hash' to be '{expected_hash}', but got '{actual_hash}'."