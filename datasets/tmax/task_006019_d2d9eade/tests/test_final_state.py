# test_final_state.py

import os
import stat
import hashlib
import pytest

def test_tls_certificates_exist_and_permissions():
    cert_path = "/home/user/tls/cert.pem"
    key_path = "/home/user/tls/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} was not created."
    assert os.path.isfile(key_path), f"Private key file {key_path} was not created."

    # Check permissions of key.pem (should be exactly 0400 / -r--------)
    st = os.stat(key_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Permissions for {key_path} are incorrect. Expected 0400, got {oct(perms)}."

def test_stage2_bin_exists_permissions_and_content():
    stage2_path = "/tmp/stage2.bin"

    assert os.path.isfile(stage2_path), f"Decrypted payload file {stage2_path} was not created."

    # Check permissions of stage2.bin (should be exactly 0700 / -rwx------)
    st = os.stat(stage2_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Permissions for {stage2_path} are incorrect. Expected 0700, got {oct(perms)}."

    # Check contents
    expected_content = b"echo 'RedTeamEvasionSuccessful'"
    with open(stage2_path, "rb") as f:
        content = f.read()

    assert content == expected_content, f"Contents of {stage2_path} do not match the expected decrypted payload."

def test_payload_hash_file():
    hash_file_path = "/home/user/payload_hash.txt"

    assert os.path.isfile(hash_file_path), f"Hash file {hash_file_path} was not created."

    expected_content = b"echo 'RedTeamEvasionSuccessful'"
    expected_hash = hashlib.sha256(expected_content).hexdigest()

    with open(hash_file_path, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Hash in {hash_file_path} is incorrect. Expected {expected_hash}, got {actual_hash}."