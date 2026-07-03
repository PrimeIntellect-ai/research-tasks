# test_final_state.py
import os
import stat
import pytest

def test_secret_file_not_overwritten():
    secret_path = "/home/user/secret.txt"
    assert os.path.isfile(secret_path), f"Secret file {secret_path} is missing."
    with open(secret_path, "r") as f:
        content = f.read().strip()
    assert content == "SAFE", "The secret file was overwritten! The extractor vulnerability was not properly fixed."

def test_extractor_executable_exists():
    extractor_path = "/home/user/project/extractor"
    assert os.path.isfile(extractor_path), f"Executable {extractor_path} is missing."
    assert os.access(extractor_path, os.X_OK), f"File {extractor_path} is not executable."

def test_extracted_files_exist():
    expected_files = ["backup.conf", "app.log", "main.c"]
    for fname in expected_files:
        path = os.path.join("/home/user/project", fname)
        assert os.path.isfile(path), f"Extracted file {path} is missing."

def test_backup_dir_and_hardlinks():
    backup_dir = "/home/user/project/backup_dir"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} is missing."

    expected_files = ["app.log", "main.c"]
    for fname in expected_files:
        orig_path = os.path.join("/home/user/project", fname)
        backup_path = os.path.join(backup_dir, fname)

        assert os.path.isfile(backup_path), f"Backup file {backup_path} is missing."

        orig_stat = os.stat(orig_path)
        backup_stat = os.stat(backup_path)

        assert orig_stat.st_ino == backup_stat.st_ino, f"{backup_path} is not a hard link to {orig_path}."
        assert orig_stat.st_nlink >= 2, f"{orig_path} does not have the expected number of hard links."

def test_success_log():
    log_path = "/home/user/project/success.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "COMPLETED", f"Expected success.log to contain 'COMPLETED', got '{content}'."