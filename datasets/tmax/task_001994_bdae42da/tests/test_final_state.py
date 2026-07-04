# test_final_state.py

import os
import subprocess
import pytest

def test_auth_service_patched():
    filepath = "/home/user/app/auth_service_fixed.cpp"
    assert os.path.isfile(filepath), f"Patched file {filepath} does not exist."

    with open(filepath, 'r') as f:
        content = f.read()

    # Check SQLi fix
    expected_query = 'std::string query = "SELECT * FROM users WHERE token = ?";'
    assert expected_query in content, "The vulnerable query was not replaced with the exact parameterized query string requested."
    assert "// Parameterized query" in content, "The comment '// Parameterized query' is missing."

    # Check Crypto fix
    assert "EVP_aes_256_cbc()" in content, "The cipher was not changed to EVP_aes_256_cbc()."
    assert '"0000000000000000"' in content or "'0', '0'" in content or "0000000000000000" in content, "The IV of 16 '0's was not found in the file."

def test_credential_rotation():
    rotated_file = "/home/user/secrets/db_config_rotated.enc"
    assert os.path.isfile(rotated_file), f"Rotated credentials file {rotated_file} does not exist."

    new_key = "6e65775f7365637265745f6b65795f31323334353637383930313233343536"
    new_iv = "30303030303030303030303030303030"

    # Decrypt the rotated file
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc",
        "-K", new_key,
        "-iv", new_iv,
        "-in", rotated_file
    ]

    result = subprocess.run(cmd, capture_output=True)
    assert result.returncode == 0, f"Failed to decrypt {rotated_file} with the new AES-256-CBC key and IV. OpenSSL error: {result.stderr.decode()}"

    plaintext = result.stdout.decode().strip()
    assert plaintext == "DB_PASS=SuperSecretPassword123!", f"Decrypted content does not match the expected plaintext. Got: {plaintext}"

def test_ssh_hardening():
    priv_key_path = "/home/user/.ssh/deploy_key"
    assert os.path.isfile(priv_key_path), f"Private key file {priv_key_path} does not exist."

    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"Authorized keys file {auth_keys_path} does not exist."

    with open(auth_keys_path, 'r') as f:
        auth_keys = f.read().strip().split('\n')

    found_hardened_key = False
    expected_prefix = 'command="/opt/deploy.sh",no-pty,no-port-forwarding ssh-ed25519 '

    for line in auth_keys:
        if line.startswith(expected_prefix):
            found_hardened_key = True
            break

    assert found_hardened_key, f"Could not find an entry in {auth_keys_path} starting exactly with '{expected_prefix}'."

def test_certificate_chain_validation():
    status_file = "/home/user/cert_status.txt"
    assert os.path.isfile(status_file), f"Certificate status file {status_file} does not exist."

    with open(status_file, 'r') as f:
        status = f.read().strip()

    assert status == "VALID", f"Expected cert_status.txt to contain exactly 'VALID', but got '{status}'."