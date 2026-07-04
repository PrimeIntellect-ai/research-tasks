# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_exists():
    """Test that the report.json file was created."""
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} is missing. The task requires generating this file."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} exists but is not a file."

def test_report_content_valid_json():
    """Test that the report is valid JSON."""
    with open(REPORT_PATH, 'r') as f:
        try:
            json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {REPORT_PATH} as JSON: {e}")

def test_report_expected_values():
    """Test that the report contains the correct extracted and derived values."""
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    # 1. Check attacker IP (Open Redirect)
    assert "attacker_ip" in data, "Missing 'attacker_ip' in report."
    expected_ip = "203.0.113.42"
    assert data["attacker_ip"] == expected_ip, f"Incorrect attacker_ip. Expected {expected_ip}, got {data['attacker_ip']}."

    # 2. Check XOR Key (Known-Plaintext Attack)
    assert "xor_key" in data, "Missing 'xor_key' in report."
    expected_key = "S3cr3t"
    assert data["xor_key"] == expected_key, f"Incorrect xor_key. Expected {expected_key}, got {data['xor_key']}."

    # 3. Check Admin Timestamp (Decrypted Token)
    assert "admin_timestamp" in data, "Missing 'admin_timestamp' in report."
    expected_ts = "1700000055"
    assert data["admin_timestamp"] == expected_ts, f"Incorrect admin_timestamp. Expected {expected_ts}, got {data['admin_timestamp']}."

    # 4. Check ReDoS Payload (Sandboxed execution)
    assert "redos_payload" in data, "Missing 'redos_payload' in report."
    expected_payload = "redirect=/home&payload=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac"
    assert data["redos_payload"] == expected_payload, f"Incorrect redos_payload. Expected {expected_payload}, got {data['redos_payload']}."