# test_final_state.py

import os
import sys
import pytest

def test_passphrase_cracked():
    passphrase_file = "/home/user/passphrase.txt"
    assert os.path.isfile(passphrase_file), f"{passphrase_file} does not exist."

    with open(passphrase_file, "r") as f:
        passphrase = f.read().strip()

    assert passphrase == "secret123", "The cracked passphrase in passphrase.txt is incorrect."

def test_admin_token_forged():
    token_file = "/home/user/admin_token.txt"
    assert os.path.isfile(token_file), f"{token_file} does not exist."

    with open(token_file, "r") as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) == 3, "The forged token does not have the correct JWT format (header.payload.signature)."

    # Import the student's auth module to test the token
    sys.path.insert(0, "/home/user/audit")
    try:
        import auth_module
    except ImportError:
        pytest.fail("Could not import auth_module.py from /home/user/audit")

    # Verify the token using the vulnerable module
    is_valid = auth_module.verify_token(token, "dummy_key")
    assert is_valid is True, "The forged token failed verification or did not grant admin access."