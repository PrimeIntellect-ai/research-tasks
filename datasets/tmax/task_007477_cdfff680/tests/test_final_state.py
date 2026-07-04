# test_final_state.py

import os
import pytest

def test_migrator_source_and_executable_exist():
    source_file = "/home/user/migrator.c"
    executable = "/home/user/migrator"

    assert os.path.isfile(source_file), f"Source file missing: {source_file}"
    assert os.path.isfile(executable), f"Executable missing: {executable}"
    assert os.access(executable, os.X_OK), f"File is not executable: {executable}"

def test_backup_archive_exists():
    archive_file = "/home/user/backup_dir/archive.tar.gz"
    assert os.path.isfile(archive_file), f"Backup archive missing: {archive_file}"
    assert os.path.getsize(archive_file) > 0, f"Backup archive is empty: {archive_file}"

def test_staging_files_exist_and_content():
    file1 = "/home/user/staging_dir/file1.txt"
    file2 = "/home/user/staging_dir/file2.txt"

    assert os.path.isfile(file1), f"Staged file missing: {file1}"
    with open(file1, "r") as f:
        assert f.read().strip() == "file1_content", f"Incorrect content in {file1}"

    assert os.path.isfile(file2), f"Staged file missing: {file2}"
    with open(file2, "r") as f:
        assert f.read().strip() == "file2_content", f"Incorrect content in {file2}"

def test_migration_log_exists_and_content():
    log_file = "/home/user/migration.log"
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    with open(log_file, "r") as f:
        content = f.read()

    expected_log = '{"status": "success", "phase": "staged"}'
    assert expected_log in content, f"Expected log entry '{expected_log}' not found in {log_file}"