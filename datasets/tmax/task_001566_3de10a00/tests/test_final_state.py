# test_final_state.py

import os
import json
import hashlib
import pytest

def test_rotate_c_exists():
    path = "/home/user/rotate.c"
    assert os.path.exists(path), f"The C program {path} is missing."
    assert os.path.isfile(path), f"The path {path} exists but is not a file."

    with open(path, "r") as f:
        content = f.read()
    assert "main" in content, f"The file {path} does not appear to be a valid C program."

def test_new_creds_json_correct():
    path = "/home/user/new_creds.json"
    assert os.path.exists(path), f"The output file {path} is missing."
    assert os.path.isfile(path), f"The path {path} exists but is not a file."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {path} does not contain valid JSON.")

    assert "status" in data, f"The JSON in {path} is missing the 'status' key."
    assert data["status"] == "rotated", f"Expected 'status' to be 'rotated', got '{data['status']}'."

    assert "new_key" in data, f"The JSON in {path} is missing the 'new_key' key."

    # Compute the expected hash
    expected_plaintext = "SecureKey2023!"
    expected_hash = hashlib.sha256(expected_plaintext.encode('utf-8')).hexdigest()

    actual_hash = data["new_key"]
    assert actual_hash == expected_hash, f"Expected 'new_key' to be '{expected_hash}', but got '{actual_hash}'."