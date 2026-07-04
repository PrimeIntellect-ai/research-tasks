# test_final_state.py

import os
import json
import pytest
import re
import subprocess
import base64
import hashlib

REPORT_PATH = "/home/user/forensics_report.json"
AUTH_KEYS_PATH = "/home/user/forensics/authorized_keys"
SYSLOG_PATH = "/home/user/forensics/syslog_dump.txt"

def test_report_exists_and_valid_json():
    """Test that the forensics report exists and is valid JSON."""
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    try:
        with open(REPORT_PATH, "r") as f:
            json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Report file {REPORT_PATH} is not valid JSON.")

def test_report_aes_key():
    """Test that the extracted AES key is correct."""
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    assert "aes_key" in data, "Key 'aes_key' missing from JSON report."

    # Derive the expected key from the syslog file
    expected_key = None
    with open(SYSLOG_PATH, "r") as f:
        for line in f:
            match = re.search(r"Key:\s*([a-f0-9]+)", line)
            if match:
                expected_key = match.group(1)
                break

    assert expected_key is not None, "Could not find expected key in syslog_dump.txt."
    assert data["aes_key"] == expected_key, f"Expected aes_key '{expected_key}', got '{data['aes_key']}'."

def test_report_stolen_token():
    """Test that the extracted stolen token is correct."""
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    assert "stolen_token" in data, "Key 'stolen_token' missing from JSON report."
    # The expected token based on the truth data
    expected_token = "secr3t_t0k3n_88192a_xyz"
    assert data["stolen_token"] == expected_token, f"Expected stolen_token '{expected_token}', got '{data['stolen_token']}'."

def test_report_malicious_key_fingerprint():
    """Test that the malicious key fingerprint is correct."""
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    assert "malicious_key_fingerprint" in data, "Key 'malicious_key_fingerprint' missing from JSON report."

    expected_fingerprint_path = "/tmp/expected_fingerprint"
    assert os.path.isfile(expected_fingerprint_path), "Expected fingerprint file missing from /tmp."

    with open(expected_fingerprint_path, "r") as f:
        expected_fingerprint = f.read().strip()

    assert data["malicious_key_fingerprint"] == expected_fingerprint, f"Expected fingerprint '{expected_fingerprint}', got '{data['malicious_key_fingerprint']}'."

def test_authorized_keys_cleaned():
    """Test that the malicious key was removed and the legitimate key remains."""
    assert os.path.isfile(AUTH_KEYS_PATH), f"{AUTH_KEYS_PATH} does not exist."

    with open(AUTH_KEYS_PATH, "r") as f:
        content = f.read()

    assert "backdoor@hacker.local" not in content, "Malicious key 'backdoor@hacker.local' was not removed from authorized_keys."
    assert "admin@local" in content, "Legitimate key 'admin@local' was incorrectly removed from authorized_keys."