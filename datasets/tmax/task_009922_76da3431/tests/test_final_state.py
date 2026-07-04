# test_final_state.py

import os
import pytest

def test_decrypt_py_exists():
    path = "/home/user/decrypt.py"
    assert os.path.isfile(path), f"Expected {path} to exist as a file. The student must write their script here."

def test_decrypted_txt_exists_and_correct():
    path = "/home/user/decrypted.txt"
    assert os.path.isfile(path), f"Expected {path} to exist as a file containing the decrypted data."

    expected_content = "FLAG{VULNERABLE_ELF_XOR_CRYPTO_BROKEN}"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == expected_content, (
        f"Content of {path} is incorrect.\n"
        f"Expected: {expected_content!r}\n"
        f"Got: {content!r}"
    )