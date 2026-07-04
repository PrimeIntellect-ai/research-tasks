# test_final_state.py

import os
import json
import pytest

LOG_PATH = "/home/user/security.log"
RUST_SRC = "/home/user/rotate.rs"
LEAKED_KEY_TXT = "/home/user/leaked_key.txt"
PAYLOAD_JSON = "/home/user/rotation_payload.json"

def get_expected_token():
    assert os.path.exists(LOG_PATH), f"Log file {LOG_PATH} is missing."
    with open(LOG_PATH, "r") as f:
        for line in f:
            if "[SANDBOX_ESCAPE]" in line and "Leaked token:" in line:
                return line.split("Leaked token:")[1].strip()
    pytest.fail("Could not find the leaked token in the security log.")

def test_rust_source_exists():
    assert os.path.isfile(RUST_SRC), f"Rust source file {RUST_SRC} is missing."

def test_leaked_key_file():
    expected_token = get_expected_token()
    assert os.path.isfile(LEAKED_KEY_TXT), f"Output file {LEAKED_KEY_TXT} is missing."

    with open(LEAKED_KEY_TXT, "r") as f:
        content = f.read().strip()

    assert content == expected_token, f"Expected {LEAKED_KEY_TXT} to contain '{expected_token}', but got '{content}'."

def test_rotation_payload_file():
    expected_token = get_expected_token()
    assert os.path.isfile(PAYLOAD_JSON), f"Output file {PAYLOAD_JSON} is missing."

    with open(PAYLOAD_JSON, "r") as f:
        content = f.read()

    expected_content = f'{{"action":"rotate","old_token":"{expected_token}","new_token":"RUST_SECURE_TOKEN_2024"}}'

    assert content == expected_content, f"Expected {PAYLOAD_JSON} to exactly match '{expected_content}', but got '{content}'."