# test_final_state.py

import os
import stat
import hashlib
import base64
import pytest

VAULT_PATH = '/home/user/vault.txt'
BINARY_PATH = '/home/user/auth_service_secure'
LOG_PATH = '/home/user/secure_hash.log'

def test_vault_permissions():
    assert os.path.exists(VAULT_PATH), f"Vault file {VAULT_PATH} does not exist."
    st = os.stat(VAULT_PATH)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Permissions of {VAULT_PATH} must be 0400, but found {oct(permissions)}."

def test_binary_exists_and_executable():
    assert os.path.exists(BINARY_PATH), f"Compiled binary {BINARY_PATH} does not exist."
    assert os.path.isfile(BINARY_PATH), f"{BINARY_PATH} is not a file."
    assert os.access(BINARY_PATH, os.X_OK), f"Compiled binary {BINARY_PATH} is not executable."

def test_secure_hash_log():
    assert os.path.exists(LOG_PATH), f"Log file {LOG_PATH} does not exist. Did you run the compiled binary?"

    with open(VAULT_PATH, 'r') as f:
        password_with_newline = f.read()

    password = password_with_newline.rstrip('\n')

    # Compute expected hash
    digest = hashlib.sha256(password.encode('utf-8')).digest()
    expected_b64 = base64.b64encode(digest).decode('utf-8')

    with open(LOG_PATH, 'r') as f:
        log_content = f.read().strip()

    assert log_content == expected_b64, f"Content of {LOG_PATH} is incorrect. Expected '{expected_b64}', got '{log_content}'."