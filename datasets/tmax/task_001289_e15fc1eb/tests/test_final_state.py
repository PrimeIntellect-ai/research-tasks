# test_final_state.py

import os
import pytest

WORKSPACE_DIR = "/home/user/workspace"
FLAG_FILE = os.path.join(WORKSPACE_DIR, "flag.txt")
TOKEN_FILE = os.path.join(WORKSPACE_DIR, "forged_token.txt")

def compute_expected_token():
    """Derives the expected token based on the vulnerable C logic."""
    target_payload = "user=auditor&role=admin"
    key = "s3cr3tk3y"

    # XOR encrypt the payload
    hex_chars = []
    for i, char in enumerate(target_payload):
        key_char = key[i % len(key)]
        xored_val = ord(char) ^ ord(key_char)
        hex_chars.append(f"{xored_val:02x}")

    hex_payload = "".join(hex_chars)

    # Append the vulnerable signature bypass
    return f"{hex_payload}.NONE"

def test_flag_file_exists_and_correct():
    assert os.path.isfile(FLAG_FILE), f"The flag file was not found at {FLAG_FILE}."

    with open(FLAG_FILE, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{alg_n0n3_byp4ss_c_impl}"
    assert expected_flag in content, (
        f"The flag file does not contain the correct flag. "
        f"Expected to find '{expected_flag}', but found '{content}'."
    )

def test_forged_token_exists_and_correct():
    assert os.path.isfile(TOKEN_FILE), f"The forged token file was not found at {TOKEN_FILE}."

    with open(TOKEN_FILE, "r") as f:
        content = f.read().strip()

    expected_token = compute_expected_token()

    assert content == expected_token, (
        f"The forged token is incorrect.\n"
        f"Expected: {expected_token}\n"
        f"Found:    {content}\n"
        f"Ensure you are XORing 'user=auditor&role=admin' with 's3cr3tk3y' and appending '.NONE'."
    )