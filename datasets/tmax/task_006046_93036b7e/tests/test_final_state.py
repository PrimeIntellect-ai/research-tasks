# test_final_state.py

import os
import pytest

def test_c_file_exists():
    """Test that the C source file exists."""
    assert os.path.isfile("/home/user/sanitize.c"), "/home/user/sanitize.c does not exist."

def test_clean_index_exists():
    """Test that the cleaned binary index exists."""
    assert os.path.isfile("/home/user/artifacts/index_clean.bin"), "/home/user/artifacts/index_clean.bin does not exist."

def test_temp_file_removed():
    """Test that the temporary file was successfully renamed/removed."""
    assert not os.path.exists("/home/user/artifacts/index_clean.bin.tmp"), "/home/user/artifacts/index_clean.bin.tmp still exists; atomic rename was likely not used."

def test_clean_index_size():
    """Test that the cleaned index size perfectly matches the original index size."""
    orig_path = "/home/user/artifacts/index.bin"
    clean_path = "/home/user/artifacts/index_clean.bin"

    assert os.path.isfile(orig_path), "Original index.bin is missing."
    orig_size = os.path.getsize(orig_path)
    clean_size = os.path.getsize(clean_path)

    assert orig_size == clean_size, f"Size mismatch: original index is {orig_size} bytes, clean index is {clean_size} bytes."

def test_clean_index_content():
    """Test that the content of the clean index has correctly sanitized paths."""
    with open("/home/user/artifacts/index_clean.bin", "rb") as f:
        data = f.read()

    assert data.startswith(b"ARTIFACT_v1\0"), "Header is incorrect in the clean index."

    # Check for presence of sanitized paths
    assert b"bin/______etc/passwd" in data, "Sanitized path 'bin/______etc/passwd' not found in clean index."
    assert b"___config/system.yml" in data, "Sanitized path '___config/system.yml' not found in clean index."
    assert b"safe/___path/file" in data, "Sanitized path 'safe/___path/file' not found in clean index."

    # Check for presence of untouched paths
    assert b"docs/readme.txt" in data, "Untouched path 'docs/readme.txt' not found in clean index."
    assert b"scripts/install.sh" in data, "Untouched path 'scripts/install.sh' not found in clean index."

    # Ensure no unsanitized sequences remain
    assert b"../" not in data, "Found unsanitized '../' sequence in the clean index."

def test_sanitized_log_content():
    """Test that the sanitized.log file exists and contains the correct entries."""
    log_path = "/home/user/artifacts/sanitized.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        log_content = [line.strip() for line in f.readlines() if line.strip()]

    expected_logs = [
        "bin/../../etc/passwd -> bin/______etc/passwd",
        "../config/system.yml -> ___config/system.yml",
        "safe/../path/file -> safe/___path/file"
    ]

    for expected in expected_logs:
        assert expected in log_content, f"Missing expected log entry: '{expected}' in {log_path}"