# test_final_state.py

import os
import hashlib

def test_recovered_credential():
    filepath = "/home/user/recovered_credential.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read()

    expected_credential = "rot-cred-9f8a7b6c5d4e3f2a1"
    assert content == expected_credential, f"Expected '{expected_credential}' in {filepath}, but got '{content}'."

def test_credential_hash():
    filepath = "/home/user/credential_hash.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_credential = "rot-cred-9f8a7b6c5d4e3f2a1"
    expected_hash = hashlib.sha256(expected_credential.encode('utf-8')).hexdigest()

    assert content == expected_hash, f"Expected hash '{expected_hash}' in {filepath}, but got '{content}'."