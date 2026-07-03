# test_final_state.py

import os
import pytest

def fnv1a(text):
    h = 0x811c9dc5
    for c in text:
        h ^= ord(c)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"

def test_forged_token_exists_and_correct():
    wordlist_path = "/home/user/wordlist.txt"
    admin_token_path = "/home/user/admin_token.txt"
    forged_token_path = "/home/user/forged_token.txt"

    assert os.path.isfile(wordlist_path), f"Wordlist file {wordlist_path} is missing."
    assert os.path.isfile(admin_token_path), f"Admin token file {admin_token_path} is missing."
    assert os.path.isfile(forged_token_path), f"Forged token file {forged_token_path} is missing. You must create it."

    with open(admin_token_path, "r") as f:
        admin_token = f.read().strip()

    with open(wordlist_path, "r") as f:
        passwords = f.read().splitlines()

    # Find the correct password from the wordlist
    correct_password = None
    for pwd in passwords:
        if fnv1a(f"admin||{pwd}||SECURE_SALT_99") == admin_token:
            correct_password = pwd
            break

    assert correct_password is not None, "Could not find a password in the wordlist that matches the admin token."

    # Calculate expected forged token
    expected_forged_token = fnv1a(f"system_root||{correct_password}||SECURE_SALT_99")

    with open(forged_token_path, "r") as f:
        actual_forged_token = f.read().strip()

    assert actual_forged_token == expected_forged_token, (
        f"The forged token in {forged_token_path} is incorrect. "
        f"Expected the token for 'system_root' using the discovered password."
    )