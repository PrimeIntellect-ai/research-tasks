# test_final_state.py

import os
import hashlib
import pytest

def test_solution_txt_exists_and_correct():
    path = "/home/user/solution.txt"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    # Recompute the expected hash from the known flag string to be robust
    expected_flag = "9a8b7c6d5e4f3g2h1i0j"
    expected_hash = hashlib.sha256(expected_flag.encode('utf-8')).hexdigest()

    assert content == expected_hash, f"The hash in {path} is incorrect. Expected {expected_hash}, got {content}."

def test_decryptor_c_exists():
    path = "/home/user/decryptor.c"
    assert os.path.exists(path), f"File {path} is missing. You must write the brute-force tool in C."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    assert len(content.strip()) > 0, f"File {path} is empty."

def test_decrypted_log_exists_and_contains_flag():
    path = "/home/user/decrypted.log"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    assert "CRIME_LOG_START{v1.0}" in content, f"The decrypted log does not contain the expected header."
    assert "FLAG: 9a8b7c6d5e4f3g2h1i0j" in content, f"The decrypted log does not contain the expected FLAG string."