# test_final_state.py

import os
import base64
import pytest

def test_crafter_source_exists():
    """Verify that the C++ source file exists."""
    source_file = "/home/user/crafter.cpp"
    assert os.path.exists(source_file), f"Source file missing: {source_file}"
    assert os.path.isfile(source_file), f"Path is not a file: {source_file}"

def test_crafter_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    executable = "/home/user/crafter"
    assert os.path.exists(executable), f"Executable missing: {executable}. Did you compile crafter.cpp?"
    assert os.path.isfile(executable), f"Path is not a file: {executable}"
    assert os.access(executable, os.X_OK), f"File is not executable: {executable}"

def test_evasion_payload_correct():
    """Verify that the evasion payload was generated correctly based on the challenge file."""
    challenge_file = "/home/user/challenge.txt"
    payload_file = "/home/user/evasion_payload.txt"

    assert os.path.exists(challenge_file), f"Challenge file missing: {challenge_file}"
    assert os.path.exists(payload_file), f"Payload file missing: {payload_file}. Did you run the executable?"

    with open(challenge_file, "r") as f:
        challenge = f.read().replace('\n', '')

    # Compute expected token
    reversed_challenge = challenge[::-1]
    expected_token = base64.b64encode(reversed_challenge.encode('utf-8')).decode('utf-8')

    # Compute expected encoded payload
    payload_str = "COMMAND:flag_captured_successfully"
    xor_key = len(challenge)
    xored_bytes = bytes([ord(c) ^ xor_key for c in payload_str])
    expected_encoded_payload = base64.b64encode(xored_bytes).decode('utf-8')

    expected_final_content = f"{expected_token}.{expected_encoded_payload}"

    with open(payload_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_final_content, (
        f"The evasion payload is incorrect.\n"
        f"Expected: {expected_final_content}\n"
        f"Got:      {actual_content}"
    )