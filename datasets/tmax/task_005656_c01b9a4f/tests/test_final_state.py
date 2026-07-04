# test_final_state.py
import os
import subprocess
import hashlib
import pytest

def test_pubkey_exists_and_valid():
    pubkey_path = "/home/user/rotation/pubkey.pem"
    assert os.path.isfile(pubkey_path), f"Public key file {pubkey_path} is missing."

    # Check if it's a valid RSA public key
    result = subprocess.run(
        ["openssl", "rsa", "-pubin", "-in", pubkey_path, "-check", "-noout"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"File {pubkey_path} is not a valid RSA public key. Output: {result.stderr}"

def test_new_secret_encrypted_properly():
    new_secret_path = "/home/user/rotation/new_secret.enc"
    private_key_path = "/home/user/certs/db_service.key"

    assert os.path.isfile(new_secret_path), f"Encrypted secret file {new_secret_path} is missing."
    assert os.path.isfile(private_key_path), f"Private key {private_key_path} is missing."

    result = subprocess.run(
        ["openssl", "pkeyutl", "-decrypt", "-inkey", private_key_path, "-in", new_secret_path],
        capture_output=True
    )
    assert result.returncode == 0, f"Failed to decrypt {new_secret_path}. Output: {result.stderr.decode()}"

    decrypted_secret = result.stdout.decode('utf-8')
    expected_secret = "SuperSecretDB99-ROTATED"
    assert decrypted_secret == expected_secret, f"Decrypted secret does not match expected. Got: {decrypted_secret}"

def test_checksum_file():
    new_secret_path = "/home/user/rotation/new_secret.enc"
    checksum_path = "/home/user/rotation/checksum.txt"

    assert os.path.isfile(new_secret_path), f"Encrypted secret file {new_secret_path} is missing."
    assert os.path.isfile(checksum_path), f"Checksum file {checksum_path} is missing."

    with open(new_secret_path, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    with open(checksum_path, "r") as f:
        checksum_content = f.read().strip()

    # The standard sha256sum output looks like: "<hash>  /path/to/file" or just "<hash>"
    # We check if the actual hash is in the file content
    assert actual_hash in checksum_content, f"Checksum file {checksum_path} does not contain the correct SHA256 hash of {new_secret_path}."

def test_deploy_log():
    new_secret_path = "/home/user/rotation/new_secret.enc"
    log_path = "/home/user/rotation/deploy.log"

    assert os.path.isfile(new_secret_path), f"Encrypted secret file {new_secret_path} is missing."
    assert os.path.isfile(log_path), f"Deploy log {log_path} is missing."

    with open(new_secret_path, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    expected_log = f"Deployment triggered with hash: {actual_hash}"

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    assert log_content == expected_log, f"Deploy log content is incorrect. Expected: '{expected_log}', Got: '{log_content}'. This indicates the environment was not properly isolated or the hash was incorrect."