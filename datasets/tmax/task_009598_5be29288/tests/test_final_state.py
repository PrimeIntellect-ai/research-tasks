# test_final_state.py

import os
import pytest

def test_forged_payload_exists_and_correct():
    payload_file = '/home/user/forged_payload.txt'

    # Assert the file was created
    assert os.path.exists(payload_file), f"Expected output file {payload_file} does not exist. Did you write the payload to the correct path?"
    assert os.path.isfile(payload_file), f"Expected {payload_file} to be a file, but it is not."

    # Derive the expected payload
    target_username = "admin_root"
    key = "s3cr"

    # Compute the expected hex token using repeating-key XOR
    expected_token = "".join(
        f"{ord(char) ^ ord(key[i % len(key)]):02x}" 
        for i, char in enumerate(target_username)
    )
    expected_payload = f"{target_username}:{expected_token}"

    # Read the actual payload
    with open(payload_file, 'r') as f:
        actual_content = f.read().strip()

    # Assert the content matches exactly
    assert actual_content == expected_payload, (
        f"The forged payload is incorrect.\n"
        f"Expected: '{expected_payload}'\n"
        f"Found:    '{actual_content}'"
    )