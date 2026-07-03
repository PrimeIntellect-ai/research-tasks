# test_final_state.py

import os
import hashlib
import subprocess
import pytest

EXPECTED_REDACTED_CONTENT = (
    "[2023-10-01T12:00:00Z] GET /login?redirect=http://evil.com&password=[REDACTED]&token=[REDACTED] HTTP/1.1\n"
    "[2023-10-01T12:05:00Z] GET /login?redirect=/home&password=[REDACTED]&token=[REDACTED] HTTP/1.1\n"
    "[2023-10-01T12:10:00Z] GET /login?token=[REDACTED]&password=[REDACTED]&redirect=/dashboard HTTP/1.1\n"
)

def test_redacted_hash():
    hash_file = "/home/user/archive/redacted_hash.txt"
    assert os.path.isfile(hash_file), f"Hash file {hash_file} does not exist."

    with open(hash_file, "r") as f:
        content = f.read().strip()

    expected_hash = hashlib.sha256(EXPECTED_REDACTED_CONTENT.encode('utf-8')).hexdigest()

    # sha256sum output is typically "<hash>  <filename>"
    assert content.startswith(expected_hash), f"The hash in {hash_file} does not match the expected SHA-256 of the redacted log."

def test_encryption_verification():
    enc_file = "/home/user/archive/access_redacted.log.enc"
    key_file = "/home/user/keys/backup.key"

    assert os.path.isfile(enc_file), f"Encrypted file {enc_file} does not exist."
    assert os.path.isfile(key_file), f"Key file {key_file} is missing."

    # Decrypt using openssl
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-pass", f"file:{key_file}",
        "-in", enc_file
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        decrypted_content = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to decrypt {enc_file}. OpenSSL error: {e.stderr}")

    assert decrypted_content == EXPECTED_REDACTED_CONTENT, "Decrypted content does not match the expected redacted log."

def test_plaintext_deletion():
    plaintext_file = "/home/user/app/logs/access_redacted.log"
    assert not os.path.exists(plaintext_file), f"Plaintext redacted log {plaintext_file} was not deleted."

def test_credential_rotation():
    config_file = "/home/user/app/config.env"
    assert os.path.isfile(config_file), f"Config file {config_file} does not exist."

    with open(config_file, "r") as f:
        lines = f.read().splitlines()

    new_password = "SuperSecurePwd2024!"
    expected_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

    expected_lines = [
        "DB_HOST=localhost",
        "DB_USER=admin",
        f"DB_PASSWORD={expected_hash}",
        "DB_PORT=5432"
    ]

    assert lines == expected_lines, f"The contents of {config_file} are incorrect. Check if the password was hashed properly and other lines remained unchanged."