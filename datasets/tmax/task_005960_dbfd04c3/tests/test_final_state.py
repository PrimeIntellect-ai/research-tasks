# test_final_state.py

import os
import hashlib
import pytest

def test_valid_cert_txt():
    """Test that /home/user/valid_cert.txt contains the correct valid certificate filename."""
    file_path = "/home/user/valid_cert.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "cert_A.crt", f"Expected 'cert_A.crt' in {file_path}, but got '{content}'."

def test_recover_rs_exists():
    """Test that /home/user/recover.rs exists."""
    file_path = "/home/user/recover.rs"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. You must write the Rust code here."

def test_payload_bin():
    """Test that /home/user/payload.bin exists and contains the correct decoded binary payload."""
    file_path = "/home/user/payload.bin"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you run your Rust program?"

    with open(file_path, "rb") as f:
        content = f.read()

    expected_bytes = b"#!/bin/bash\necho 'pwned'"
    assert content == expected_bytes, f"Payload content in {file_path} does not match the expected binary data."

    # Also verify the checksum just to be absolutely sure
    sha256_hash = hashlib.sha256(content).hexdigest()
    expected_hash = "568371353f868c2f2ce47754b5dfd4e68e0a81665a5d123e42fecfc32f41b315"
    assert sha256_hash == expected_hash, f"Expected SHA256 {expected_hash}, but got {sha256_hash}."