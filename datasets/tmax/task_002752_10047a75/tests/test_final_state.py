# test_final_state.py

import os
import pytest

def test_investigate_script_exists():
    script_path = "/home/user/investigate.rs"
    assert os.path.isfile(script_path), f"The script {script_path} was not created."

def test_decoded_payload_exists_and_correct():
    payload_path = "/home/user/decoded_payload.txt"
    assert os.path.isfile(payload_path), f"The file {payload_path} was not created."

    with open(payload_path, 'r') as f:
        content = f.read()

    expected_payload = '{"user": "admin", "privilege": "escalated"}'
    assert content == expected_payload, f"The decoded payload is incorrect. Expected '{expected_payload}', got '{content}'."