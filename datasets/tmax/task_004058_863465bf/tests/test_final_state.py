# test_final_state.py
import os
import socket
import hashlib
import pytest
import glob

def test_storage_directory_exists():
    storage_dir = "/home/user/upload_service/storage"
    assert os.path.isdir(storage_dir), f"Directory {storage_dir} does not exist."

def test_required_files_exist():
    base_dir = "/home/user/upload_service"
    required_files = ["upload.proto", "server.py", "client.py", "test.bin", "result.txt"]
    for f in required_files:
        path = os.path.join(base_dir, f)
        assert os.path.isfile(path), f"Required file {path} is missing."

def test_test_bin_size_and_checksum():
    test_bin_path = "/home/user/upload_service/test.bin"
    size = os.path.getsize(test_bin_path)
    # The spec says "generate a 5MB random binary file". We check if it's roughly 5MB.
    # 5MB could be 5,000,000 or 5,242,880 bytes.
    assert size >= 5000000, f"{test_bin_path} is smaller than 5MB."

    # Read client output
    result_path = "/home/user/upload_service/result.txt"
    with open(result_path, "r") as f:
        result_content = f.read().strip()

    # Extract the SHA-256 hex digest (64 hex characters)
    # It might be embedded in some text, so let's look for a 64-char hex string
    import re
    match = re.search(r'[a-fA-F0-9]{64}', result_content)
    assert match is not None, f"Could not find a valid SHA-256 checksum in {result_path}."
    client_sha256 = match.group(0).lower()

    # Compute actual SHA-256 of test.bin
    hasher = hashlib.sha256()
    with open(test_bin_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    actual_sha256 = hasher.hexdigest()

    assert client_sha256 == actual_sha256, f"Checksum in {result_path} ({client_sha256}) does not match actual SHA-256 of {test_bin_path} ({actual_sha256})."

def test_server_listening():
    # Check if port 50051 is open
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex(('127.0.0.1', 50051))
        assert result == 0, "Server is not listening on port 50051."
    finally:
        s.close()

def test_uploaded_file_in_storage():
    storage_dir = "/home/user/upload_service/storage"
    test_bin_path = "/home/user/upload_service/test.bin"

    hasher = hashlib.sha256()
    with open(test_bin_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    expected_sha256 = hasher.hexdigest()

    # Find if any file in storage matches the test.bin checksum
    found = False
    for filename in os.listdir(storage_dir):
        filepath = os.path.join(storage_dir, filename)
        if os.path.isfile(filepath):
            file_hasher = hashlib.sha256()
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    file_hasher.update(chunk)
            if file_hasher.hexdigest() == expected_sha256:
                found = True
                break

    assert found, "Could not find the uploaded test file in the storage directory with the matching checksum."