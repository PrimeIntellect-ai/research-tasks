# test_final_state.py

import os
import pytest

def test_forged_token_correct():
    token_path = '/home/user/forged_token.txt'
    assert os.path.isfile(token_path), f"File {token_path} does not exist."

    with open(token_path, 'r') as f:
        token = f.read().strip()

    # Recompute the expected token for 'admin' based on the logic:
    # ''.join([format(ord(c) ^ 0x42, '02x') for c in 'admin'])
    expected_token = ''.join([format(ord(c) ^ 0x42, '02x') for c in 'admin'])

    assert token == expected_token, f"Token in {token_path} is incorrect. Expected {expected_token}, got {token}."

def test_ssh_keys_exist_and_match():
    auth_keys_path = '/home/user/.ssh/authorized_keys'
    pub_key_path = '/home/user/new_key.pub'
    priv_key_path = '/home/user/new_key'

    assert os.path.isfile(auth_keys_path), f"File {auth_keys_path} does not exist. Path traversal may have failed."
    assert os.path.isfile(pub_key_path), f"File {pub_key_path} does not exist."
    assert os.path.isfile(priv_key_path), f"File {priv_key_path} does not exist."

    with open(auth_keys_path, 'r') as f:
        auth_keys_content = f.read().strip()

    with open(pub_key_path, 'r') as f:
        pub_key_content = f.read().strip()

    assert auth_keys_content == pub_key_content, "The contents of authorized_keys do not match the generated public key."
    assert len(pub_key_content) > 0, "The public key file is empty."

def test_private_key_validity():
    priv_key_path = '/home/user/new_key'
    assert os.path.isfile(priv_key_path), f"File {priv_key_path} does not exist."

    with open(priv_key_path, 'r') as f:
        priv_key_content = f.read().strip()

    assert "PRIVATE KEY" in priv_key_content, f"The file {priv_key_path} does not appear to be a valid private key."