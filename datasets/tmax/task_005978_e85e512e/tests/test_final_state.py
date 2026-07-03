# test_final_state.py
import os
import hashlib
import pytest

def test_processed_logs_exist():
    processed_dir = "/home/user/processed_logs"
    for i in range(1, 4):
        file_path = os.path.join(processed_dir, f"error_app.log.{i}")
        assert os.path.isfile(file_path), f"Expected processed log file {file_path} is missing."

def test_error_log_contents():
    processed_dir = "/home/user/processed_logs"

    # Log 1
    file1 = os.path.join(processed_dir, "error_app.log.1")
    if os.path.exists(file1):
        with open(file1, "r") as f:
            content1 = f.read()
        assert "[ERROR] Database connection failed" in content1, "Log 1 missing expected error header."
        assert "ConnectionRefusedError" in content1, "Log 1 missing expected multi-line error content."
        assert "[INFO]" not in content1, "Log 1 incorrectly contains non-error lines."

    # Log 2
    file2 = os.path.join(processed_dir, "error_app.log.2")
    if os.path.exists(file2):
        with open(file2, "r") as f:
            content2 = f.read()
        assert "[ERROR] Out of memory" in content2, "Log 2 missing expected error header."
        assert "Requested: 8GB" in content2, "Log 2 missing expected multi-line error content."
        assert "[DEBUG]" not in content2, "Log 2 incorrectly contains non-error lines."

    # Log 3
    file3 = os.path.join(processed_dir, "error_app.log.3")
    if os.path.exists(file3):
        with open(file3, "r") as f:
            content3 = f.read()
        assert "[ERROR] Disk full" in content3, "Log 3 missing expected error header."
        assert "Please clear space" in content3, "Log 3 missing expected multi-line error content."
        assert "[WARN]" not in content3, "Log 3 incorrectly contains non-error lines."

def test_manifest_checksums():
    processed_dir = "/home/user/processed_logs"
    manifest_path = os.path.join(processed_dir, "manifest.txt")
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    # Compute expected checksums based on actual file contents
    expected_checksums = {}
    for i in range(1, 4):
        file_path = os.path.join(processed_dir, f"error_app.log.{i}")
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                expected_checksums[f"error_app.log.{i}"] = hashlib.sha256(f.read()).hexdigest()

    with open(manifest_path, "r") as f:
        manifest_content = f.read()

    for filename, expected_hash in expected_checksums.items():
        assert expected_hash in manifest_content, f"Checksum {expected_hash} for {filename} is missing in manifest.txt."
        assert filename in manifest_content, f"Filename {filename} is missing in manifest.txt."

def test_latest_error_symlink():
    symlink_path = "/home/user/processed_logs/latest_error.log"
    assert os.path.islink(symlink_path), f"{symlink_path} is missing or is not a symbolic link."

    target = os.readlink(symlink_path)
    expected_targets = ["error_app.log.3", "/home/user/processed_logs/error_app.log.3"]
    assert target in expected_targets, f"Symlink points to '{target}' instead of 'error_app.log.3'."