# test_final_state.py

import os
import re
import pytest

def test_executable_exists():
    executable_path = "/home/user/cost_optimizer"
    assert os.path.isfile(executable_path), f"Executable missing: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_backup_files():
    backup_files = {
        "/home/user/storage_backup/large1.bin": 150000,
        "/home/user/storage_backup/large2.bin": 200000,
    }
    for f_path, expected_size in backup_files.items():
        assert os.path.isfile(f_path), f"Backup file missing: {f_path}"
        actual_size = os.path.getsize(f_path)
        assert actual_size == expected_size, f"Backup file {f_path} has incorrect size: {actual_size} != {expected_size}"

def test_staged_files():
    staged_files = {
        "/home/user/archive_staging/large1.bin": 150000,
        "/home/user/archive_staging/large2.bin": 200000,
    }
    for f_path, expected_size in staged_files.items():
        assert os.path.isfile(f_path), f"Staged file missing: {f_path}"
        actual_size = os.path.getsize(f_path)
        assert actual_size == expected_size, f"Staged file {f_path} has incorrect size: {actual_size} != {expected_size}"

def test_original_large_files_removed():
    removed_files = [
        "/home/user/cloud_storage/bucketA/large1.bin",
        "/home/user/cloud_storage/bucketB/large2.bin",
    ]
    for f_path in removed_files:
        assert not os.path.exists(f_path), f"Original large file should have been removed: {f_path}"

def test_original_small_files_remain():
    small_files = {
        "/home/user/cloud_storage/bucketA/small1.txt": 50000,
        "/home/user/cloud_storage/bucketB/small2.txt": 99999,
    }
    for f_path, expected_size in small_files.items():
        assert os.path.isfile(f_path), f"Small file should still exist: {f_path}"
        actual_size = os.path.getsize(f_path)
        assert actual_size == expected_size, f"Small file {f_path} has incorrect size: {actual_size} != {expected_size}"

def test_audit_log():
    log_path = "/home/user/finops_audit.log"
    assert os.path.isfile(log_path), f"Audit log missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Audit log should contain exactly 2 lines, found {len(lines)}"

    pattern1 = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC\] STAGED \/home\/user\/cloud_storage\/bucketA\/large1\.bin 150000 bytes$"
    pattern2 = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC\] STAGED \/home\/user\/cloud_storage\/bucketB\/large2\.bin 200000 bytes$"

    match1 = any(re.match(pattern1, line) for line in lines)
    match2 = any(re.match(pattern2, line) for line in lines)

    assert match1, "Audit log missing or incorrect format for large1.bin entry"
    assert match2, "Audit log missing or incorrect format for large2.bin entry"