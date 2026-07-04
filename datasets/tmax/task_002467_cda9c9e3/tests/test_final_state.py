# test_final_state.py

import os
import stat
import pytest

CRACK_PY_PATH = "/home/user/crack.py"
PASSPHRASE_TXT_PATH = "/home/user/passphrase.txt"
DECRYPTED_KEY_PATH = "/home/user/decrypted_id_rsa"
EXPECTED_PASSPHRASE = "7492admin"

def test_crack_script_exists():
    assert os.path.isfile(CRACK_PY_PATH), f"The script {CRACK_PY_PATH} is missing."

def test_passphrase_file():
    assert os.path.isfile(PASSPHRASE_TXT_PATH), f"The file {PASSPHRASE_TXT_PATH} is missing."
    with open(PASSPHRASE_TXT_PATH, "r") as f:
        content = f.read().strip()
    assert content == EXPECTED_PASSPHRASE, f"The passphrase in {PASSPHRASE_TXT_PATH} is incorrect."

def test_decrypted_key_exists():
    assert os.path.isfile(DECRYPTED_KEY_PATH), f"The decrypted key file {DECRYPTED_KEY_PATH} is missing."

def test_decrypted_key_permissions():
    assert os.path.isfile(DECRYPTED_KEY_PATH), f"The decrypted key file {DECRYPTED_KEY_PATH} is missing."
    st = os.stat(DECRYPTED_KEY_PATH)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions on {DECRYPTED_KEY_PATH} are {oct(perms)}, expected 0o600."

def test_decrypted_key_unencrypted():
    assert os.path.isfile(DECRYPTED_KEY_PATH), f"The decrypted key file {DECRYPTED_KEY_PATH} is missing."
    with open(DECRYPTED_KEY_PATH, "r") as f:
        content = f.read()
    assert "PRIVATE KEY" in content, f"The file {DECRYPTED_KEY_PATH} does not appear to be a private key."
    assert "ENCRYPTED" not in content, f"The file {DECRYPTED_KEY_PATH} is still encrypted."