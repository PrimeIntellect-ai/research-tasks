# test_final_state.py

import os
import json
import pytest

FINDINGS_FILE = "/home/user/findings.json"

def test_findings_file_exists():
    assert os.path.isfile(FINDINGS_FILE), f"The file {FINDINGS_FILE} does not exist."

def test_findings_json_format():
    with open(FINDINGS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{FINDINGS_FILE} is not a valid JSON file.")

    assert isinstance(data, dict), "The JSON root must be a dictionary."

    expected_keys = {"attacker_ip", "attacker_user", "valid_token"}
    actual_keys = set(data.keys())
    assert expected_keys == actual_keys, f"JSON keys do not match. Expected {expected_keys}, found {actual_keys}."

def test_attacker_details():
    with open(FINDINGS_FILE, 'r') as f:
        data = json.load(f)

    assert data["attacker_ip"] == "10.0.5.55", "Incorrect attacker_ip."
    assert data["attacker_user"] == "www-data", "Incorrect attacker_user."

def test_valid_token():
    with open(FINDINGS_FILE, 'r') as f:
        data = json.load(f)

    token = data["valid_token"]
    assert isinstance(token, str), "valid_token must be a string."
    assert token.startswith("ADM-"), "valid_token must start with 'ADM-'."

    # Calculate checksum of the rest of the string
    rest_of_token = token[4:]
    checksum = sum(ord(c) for c in rest_of_token)

    expected_checksum = 0x15e  # 350
    assert checksum == expected_checksum, f"Token checksum is {checksum}, but expected {expected_checksum}."