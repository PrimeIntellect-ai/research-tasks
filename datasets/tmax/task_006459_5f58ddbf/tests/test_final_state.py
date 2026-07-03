# test_final_state.py
import json
import os
import pytest

REPORT_PATH = "/home/user/report.json"
TRUTH_COMMIT_PATH = "/tmp/truth_commit.txt"

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"The report file was not found at {REPORT_PATH}."

def test_report_contents():
    assert os.path.exists(REPORT_PATH), f"Cannot check contents, {REPORT_PATH} is missing."

    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

    assert isinstance(report, dict), "The report JSON should be an object (dictionary)."

    # Load truth data
    assert os.path.exists(TRUTH_COMMIT_PATH), f"Truth file {TRUTH_COMMIT_PATH} is missing."
    with open(TRUTH_COMMIT_PATH, "r") as f:
        expected_hash = f.read().strip()

    expected_payload_hex = b"DATA:\xe2\x98\xa0\x00".hex()
    expected_error_string = "ERR_STATE_A9F3B2C1D4"

    # Validate payload
    assert "crashing_payload_hex" in report, "Missing 'crashing_payload_hex' key in the report."
    actual_payload = str(report["crashing_payload_hex"]).lower()
    assert actual_payload == expected_payload_hex.lower(), \
        f"Incorrect crashing_payload_hex. Expected {expected_payload_hex.lower()}, got {actual_payload}."

    # Validate error string
    assert "error_state_string" in report, "Missing 'error_state_string' key in the report."
    actual_error_string = report["error_state_string"]
    assert actual_error_string == expected_error_string, \
        f"Incorrect error_state_string. Expected {expected_error_string}, got {actual_error_string}."

    # Validate bad commit hash
    assert "bad_commit_hash" in report, "Missing 'bad_commit_hash' key in the report."
    actual_hash = report["bad_commit_hash"]
    assert actual_hash == expected_hash, \
        f"Incorrect bad_commit_hash. Expected {expected_hash}, got {actual_hash}."