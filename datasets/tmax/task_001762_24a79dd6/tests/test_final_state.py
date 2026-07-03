# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    assert os.path.isdir("/home/user/tracker"), "Rust project directory /home/user/tracker does not exist."
    assert os.path.isfile("/home/user/tracker/Cargo.toml"), "Cargo.toml is missing in /home/user/tracker."
    assert os.path.isfile("/home/user/tracker/src/main.rs"), "src/main.rs is missing in /home/user/tracker."

def test_compiled_binary_exists():
    binary_path = "/home/user/tracker/target/debug/tracker"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}. Did you run 'cargo build'?"
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable."

def test_app1_backup_correct():
    backup_path = "/home/user/backup/app1.conf"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

    with open(backup_path, "r") as f:
        content = f.read()

    expected_content = "USER=admin\nPASSWORD=REDACTED\nPORT=8080\n"
    # Allow for trailing newlines or slight differences in newline handling, 
    # but exact lines must match.
    lines = [line.strip() for line in content.strip().split("\n")]
    expected_lines = ["USER=admin", "PASSWORD=REDACTED", "PORT=8080"]

    assert lines == expected_lines, f"Content of {backup_path} is incorrect. Expected {expected_lines}, got {lines}."

def test_app3_backup_correct():
    backup_path = "/home/user/backup/subdir/app3.conf"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist. Make sure intermediate directories are created."

    with open(backup_path, "r") as f:
        content = f.read()

    lines = [line.strip() for line in content.strip().split("\n")]
    expected_lines = ["DB_HOST=localhost", "PASSWORD=REDACTED", "DB_NAME=test"]

    assert lines == expected_lines, f"Content of {backup_path} is incorrect. Expected {expected_lines}, got {lines}."

def test_app2_backup_does_not_exist():
    backup_path = "/home/user/backup/app2.conf"
    assert not os.path.exists(backup_path), f"Backup file {backup_path} should NOT exist because its modification time is older than the threshold."

def test_no_spurious_backup_files():
    # Ensure loop didn't cause deeply nested subdir/subdir/subdir... backups
    nested_path = "/home/user/backup/subdir/subdir"
    assert not os.path.exists(nested_path), "Found nested 'subdir/subdir' in backup, which indicates symlink loop was not properly prevented."