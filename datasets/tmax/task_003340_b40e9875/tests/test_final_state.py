# test_final_state.py

import os
import hmac
import hashlib

def test_admin_token():
    secret_path = "/home/user/keys/secret.key"
    token_path = "/home/user/admin_token.txt"

    assert os.path.exists(secret_path), f"Secret key file missing: {secret_path}"
    assert os.path.exists(token_path), f"Admin token file missing: {token_path}"

    with open(secret_path, "rb") as f:
        key = f.read()

    expected_hmac = hmac.new(key, b"admin-access-request", hashlib.sha256).hexdigest()

    with open(token_path, "r") as f:
        actual_hmac = f.read().strip()

    assert actual_hmac == expected_hmac, f"The token in {token_path} does not match the expected HMAC-SHA256 signature."

def test_ssh_hardening():
    priv_key = "/home/user/.ssh/ops_key"
    pub_key = "/home/user/.ssh/ops_key.pub"
    auth_keys = "/home/user/.ssh/authorized_keys"

    assert os.path.exists(priv_key), f"Private key missing: {priv_key}"
    assert os.path.exists(pub_key), f"Public key missing: {pub_key}"
    assert os.path.exists(auth_keys), f"Authorized keys file missing: {auth_keys}"

    with open(pub_key, "r") as f:
        pub_content = f.read().strip()

    # The public key usually contains 'ssh-ed25519 <base64> [comment]'
    # Ensure the exact restriction string is prepended.
    expected_entry = f'restrict,from="10.0.0.0/8" {pub_content}'

    with open(auth_keys, "r") as f:
        auth_content = f.read().splitlines()

    assert any(expected_entry == line.strip() for line in auth_content), \
        f"The authorized_keys file does not contain the correctly restricted public key entry."

def test_header_audit():
    log_path = "/home/user/header_audit.log"

    assert os.path.exists(log_path), f"Audit log missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}"

    expected_lines = {
        "MISSING: X-Frame-Options",
        "MISSING: Strict-Transport-Security"
    }

    actual_lines = set(lines)
    assert actual_lines == expected_lines, \
        f"Audit log contents do not match expected. Expected: {expected_lines}, Found: {actual_lines}"