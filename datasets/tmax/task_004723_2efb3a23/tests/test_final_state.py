# test_final_state.py

import os
import stat
import hashlib
import pytest

DECRYPTED_KEY_PATH = "/home/user/decrypted_key.pem"
KEY_HASH_PATH = "/home/user/key_hash.txt"

def test_decrypted_key_exists_and_unencrypted():
    assert os.path.isfile(DECRYPTED_KEY_PATH), f"The decrypted key file {DECRYPTED_KEY_PATH} does not exist."

    with open(DECRYPTED_KEY_PATH, "r") as f:
        content = f.read()

    assert "BEGIN RSA PRIVATE KEY" in content, f"The file {DECRYPTED_KEY_PATH} does not appear to be a valid RSA private key."
    assert "ENCRYPTED" not in content, f"The file {DECRYPTED_KEY_PATH} is still encrypted."

def test_decrypted_key_permissions():
    assert os.path.isfile(DECRYPTED_KEY_PATH), f"The decrypted key file {DECRYPTED_KEY_PATH} does not exist."

    file_stat = os.stat(DECRYPTED_KEY_PATH)
    mode = stat.S_IMODE(file_stat.st_mode)

    # Acceptable secure permissions for SSH keys: 0600 or 0400
    assert mode in (0o600, 0o400), f"The file {DECRYPTED_KEY_PATH} has insecure permissions: {oct(mode)}. Expected 0o600 or 0o400."

def test_key_hash_correct():
    assert os.path.isfile(DECRYPTED_KEY_PATH), f"The decrypted key file {DECRYPTED_KEY_PATH} does not exist."
    assert os.path.isfile(KEY_HASH_PATH), f"The key hash file {KEY_HASH_PATH} does not exist."

    with open(DECRYPTED_KEY_PATH, "rb") as f:
        key_data = f.read()

    expected_hash = hashlib.sha256(key_data).hexdigest()

    with open(KEY_HASH_PATH, "r") as f:
        stored_hash = f.read().strip()

    assert stored_hash == expected_hash, f"The hash in {KEY_HASH_PATH} ({stored_hash}) does not match the actual SHA256 hash of the decrypted key ({expected_hash})."