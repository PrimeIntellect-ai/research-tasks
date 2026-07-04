# test_final_state.py

import os
import json
import hashlib
import pytest

REPORT_FILE = "/home/user/audit_report.json"
SERVER_BIN_PATH = "/home/user/service/server"

def test_audit_report_exists_and_valid():
    assert os.path.isfile(REPORT_FILE), f"The audit report was not found at {REPORT_FILE}"

    with open(REPORT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {REPORT_FILE} does not contain valid JSON.")

    assert "attacker_ip" in data, "Missing 'attacker_ip' key in the JSON report."
    assert "listening_port" in data, "Missing 'listening_port' key in the JSON report."
    assert "binary_sha256" in data, "Missing 'binary_sha256' key in the JSON report."

    assert data["attacker_ip"] == "10.55.20.13", f"Expected attacker_ip to be '10.55.20.13', got '{data['attacker_ip']}'"

    assert isinstance(data["listening_port"], int), f"Expected listening_port to be an integer, got {type(data['listening_port']).__name__}"
    assert data["listening_port"] == 8443, f"Expected listening_port to be 8443, got {data['listening_port']}"

    # Compute expected sha256 dynamically
    assert os.path.isfile(SERVER_BIN_PATH), f"The server binary was not found at {SERVER_BIN_PATH}"
    with open(SERVER_BIN_PATH, "rb") as f:
        bin_data = f.read()
    expected_hash = hashlib.sha256(bin_data).hexdigest()

    assert data["binary_sha256"] == expected_hash, f"Expected binary_sha256 to be '{expected_hash}', got '{data['binary_sha256']}'"