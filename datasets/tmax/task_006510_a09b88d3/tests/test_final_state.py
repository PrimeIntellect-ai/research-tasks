# test_final_state.py

import os
import stat
import json
import random
import pytest

def get_expected_admin_token():
    # Recompute the token based on the known seed from the setup
    random.seed(1715000000)
    _ = random.randint(10000000, 99999999) # guest token
    admin_val = random.randint(10000000, 99999999)
    return f"admin-{admin_val}"

def test_admin_token_recovered():
    token_file = "/home/user/admin_token.txt"
    assert os.path.exists(token_file), f"File {token_file} does not exist."
    assert os.path.isfile(token_file), f"{token_file} is not a file."

    with open(token_file, "r") as f:
        content = f.read().strip()

    expected_token = get_expected_admin_token()
    assert content == expected_token, f"Recovered token in {token_file} is incorrect."

def test_ssh_key_generated():
    priv_key = "/home/user/.ssh/id_ed25519_admin"
    pub_key = "/home/user/.ssh/id_ed25519_admin.pub"

    assert os.path.exists(priv_key), f"Private key file {priv_key} does not exist."
    assert os.path.isfile(priv_key), f"{priv_key} is not a file."

    # Check permissions (0600)
    mode = stat.S_IMODE(os.stat(priv_key).st_mode)
    assert mode == 0o600, f"Permissions for {priv_key} are not 0600, got {oct(mode)}."

    assert os.path.exists(pub_key), f"Public key file {pub_key} does not exist."
    assert os.path.isfile(pub_key), f"{pub_key} is not a file."

def test_key_rotation_payload():
    payload_file = "/home/user/key_rotation_payload.json"
    pub_key_file = "/home/user/.ssh/id_ed25519_admin.pub"

    assert os.path.exists(payload_file), f"Payload file {payload_file} does not exist."
    assert os.path.isfile(payload_file), f"{payload_file} is not a file."

    with open(payload_file, "r") as f:
        try:
            payload = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{payload_file} does not contain valid JSON.")

    assert "token" in payload, f"'token' key missing in {payload_file}."
    assert "ssh_key" in payload, f"'ssh_key' key missing in {payload_file}."

    expected_token = get_expected_admin_token()
    assert payload["token"] == expected_token, f"Token in payload does not match the expected admin token."

    with open(pub_key_file, "r") as f:
        pub_key_content = f.read().rstrip('\n')

    assert payload["ssh_key"] == pub_key_content, "SSH key in payload does not match the public key file content."