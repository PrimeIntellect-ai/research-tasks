# test_final_state.py

import os
import hashlib

def test_analyze_go_exists():
    path = "/home/user/analyze.go"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "package main" in content or "package " in content, f"{path} does not look like valid Go code."

def test_password_txt_content():
    path = "/home/user/password.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read()

    expected_password = "V0rt3x_47"
    assert content == expected_password, f"Expected password.txt to contain '{expected_password}', but got '{content}'"

def test_payload_bin_extracted_and_hash_matches():
    bin_path = "/home/user/payload.bin"
    hash_path = "/home/user/payload.sha256"

    assert os.path.isfile(bin_path), f"Missing file: {bin_path}"
    assert os.path.isfile(hash_path), f"Missing file: {hash_path}"

    with open(hash_path, "r") as f:
        expected_hash_line = f.read().strip()
        expected_hash = expected_hash_line.split()[0]

    sha256 = hashlib.sha256()
    with open(bin_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    actual_hash = sha256.hexdigest()

    assert actual_hash == expected_hash, f"SHA256 of {bin_path} ({actual_hash}) does not match expected hash ({expected_hash})"