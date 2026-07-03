# test_final_state.py

import os
import json
import hashlib
import pytest

def test_rotation_summary_exists():
    path = "/home/user/rotation_summary.json"
    assert os.path.isfile(path), f"The file {path} does not exist. Ensure you have created the reporting file."

def test_rotation_summary_format_and_content():
    path = "/home/user/rotation_summary.json"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {path} does not contain valid JSON.")

    assert "cracked_password" in data, "The JSON file is missing the 'cracked_password' key."
    assert "private_key_checksum" in data, "The JSON file is missing the 'private_key_checksum' key."

    expected_password = "B4sti0n_M4st3r_2022!"
    assert data["cracked_password"] == expected_password, f"The cracked password reported is incorrect."

def test_ssh_key_generated_and_checksum_matches():
    priv_key_path = "/home/user/.ssh/id_ed25519"
    summary_path = "/home/user/rotation_summary.json"

    assert os.path.isfile(priv_key_path), f"The private key {priv_key_path} does not exist. Did the rotation script run successfully?"
    assert os.path.isfile(summary_path), f"The file {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {summary_path} does not contain valid JSON.")

    reported_checksum = data.get("private_key_checksum")
    assert reported_checksum is not None, "The 'private_key_checksum' key is missing from the summary JSON."

    # Calculate actual checksum
    sha256_hash = hashlib.sha256()
    with open(priv_key_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    actual_checksum = sha256_hash.hexdigest()

    assert reported_checksum == actual_checksum, f"The reported private key checksum ({reported_checksum}) does not match the actual checksum of {priv_key_path} ({actual_checksum})."

def test_ssh_authorized_keys_updated():
    pub_key_path = "/home/user/.ssh/id_ed25519.pub"
    auth_keys_path = "/home/user/.ssh/authorized_keys"

    assert os.path.isfile(pub_key_path), f"The public key {pub_key_path} does not exist."
    assert os.path.isfile(auth_keys_path), f"The authorized_keys file {auth_keys_path} does not exist."

    with open(pub_key_path, 'r') as f:
        pub_key_content = f.read().strip()

    with open(auth_keys_path, 'r') as f:
        auth_keys_content = f.read().strip()

    assert pub_key_content == auth_keys_content, "The authorized_keys file does not match the newly generated public key."