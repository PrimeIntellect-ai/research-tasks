# test_final_state.py

import os
import pytest

def test_source_code_exists():
    path = "/home/user/incremental_backup.c"
    assert os.path.exists(path), f"Source file {path} is missing."
    assert os.path.isfile(path), f"{path} should be a regular file."

def test_executable_exists():
    path = "/home/user/incremental_backup"
    assert os.path.exists(path), f"Executable {path} is missing."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_backup_err_content():
    path = "/home/user/backup.err"
    assert os.path.exists(path), f"Error log {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "LOCKED: /home/user/data_source/logs/active.log"
    assert expected in content, f"Expected '{expected}' to be in {path}, but got: {content}"

def test_backup_out_content():
    path = "/home/user/backup.out"
    assert os.path.exists(path), f"Output file {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Required blocks
    block_a = "---FILE: /home/user/data_source/config/new_app.conf---\nrecent config data\n"
    block_b = "---FILE: /home/user/data_source/logs/syslog.1---\nlog entry 1\n"

    assert block_a in content, f"Expected block for new_app.conf is missing or malformed in {path}."
    assert block_b in content, f"Expected block for syslog.1 is missing or malformed in {path}."

    # Excluded blocks
    assert "old config data" not in content, f"File app.conf should have been excluded based on timestamp."
    assert "active log" not in content, f"File active.log should have been skipped because it was locked."
    assert "---FILE: /home/user/data_source/logs/active.log---" not in content, "active.log should be skipped."
    assert "---FILE: /home/user/data_source/config/app.conf---" not in content, "app.conf should be skipped."