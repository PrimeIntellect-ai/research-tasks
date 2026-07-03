# test_final_state.py

import os
import hashlib
import pytest

def test_decrypt_c_exists():
    file_path = "/home/user/decrypt.c"
    assert os.path.isfile(file_path), f"File not found: {file_path}. You must write the decryption logic in C."

def test_recovered_token():
    file_path = "/home/user/recovered_token.txt"
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, "r") as f:
        content = f.read()

    expected_token = "SuperSecretAdminPassword99"
    assert content == expected_token, f"The recovered token is incorrect or contains extra characters/newlines. Expected '{expected_token}', got '{content}'."

def test_token_hash():
    file_path = "/home/user/token_hash.txt"
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_token = b"SuperSecretAdminPassword99"
    expected_hash = hashlib.sha256(expected_token).hexdigest()

    assert content == expected_hash, f"The token hash is incorrect. Expected '{expected_hash}', got '{content}'."