# test_final_state.py

import os
import pytest

def test_decrypted_payload_exists_and_correct():
    """Verify that the decrypted payload file exists and contains the correct flag."""
    payload_path = "/home/user/decrypted_payload.txt"

    # Check if the file exists
    assert os.path.exists(payload_path), f"The payload file was not found at {payload_path}. Did you successfully execute the binary?"
    assert os.path.isfile(payload_path), f"Expected {payload_path} to be a file, but it is not."

    # Check the contents of the file
    with open(payload_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{m4lw4r3_r3v3rs3d_succ3ssfullY}"
    assert content == expected_flag, f"The payload file does not contain the correct flag. Found: '{content}'"