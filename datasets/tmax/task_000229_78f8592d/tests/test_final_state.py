# test_final_state.py

import os
import pytest

def test_decrypt_script_exists_and_executable():
    path = "/home/user/decrypt.sh"
    assert os.path.isfile(path), f"Missing script: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

def test_decrypt_script_is_pure_bash():
    path = "/home/user/decrypt.sh"
    assert os.path.isfile(path), f"Missing script: {path}"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    # Check that it doesn't use forbidden languages
    assert "python" not in content, "The decryption script must be written in Bash, not Python."
    assert "ruby" not in content, "The decryption script must be written in Bash, not Ruby."
    assert "perl" not in content, "The decryption script must be written in Bash, not Perl."

def test_decrypted_token_content():
    path = "/home/user/decrypted_token.txt"
    assert os.path.isfile(path), f"Missing decrypted token file: {path}"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_plaintext = "ACCESS_GRANTED_8839201_SYSTEM"
    assert content == expected_plaintext, f"Decrypted token content is incorrect. Expected '{expected_plaintext}', got '{content}'"