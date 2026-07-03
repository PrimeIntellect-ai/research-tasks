# test_final_state.py

import os
import pytest

def test_analyzer_executable_exists():
    """Verify that the compiled C program exists and is executable."""
    executable_path = '/home/user/analyzer'
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_config_backup_exists_and_matches():
    """Verify that config.ini.bak exists and matches the original config.ini."""
    original_path = '/home/user/net_data/config.ini'
    backup_path = '/home/user/config.ini.bak'

    assert os.path.isfile(backup_path), f"Backup file {backup_path} is missing."
    assert os.path.isfile(original_path), f"Original file {original_path} is missing."

    with open(original_path, 'r') as f_orig, open(backup_path, 'r') as f_bak:
        original_content = f_orig.read()
        backup_content = f_bak.read()

    assert backup_content == original_content, "The backup file contents do not match the original config.ini."

def test_resolution_log_exists_and_content():
    """Verify that resolution.log exists and contains the correct extracted information."""
    log_path = '/home/user/resolution.log'
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_content = "MountPoint: /home/user/net_data\nForwardedPort: 8088"
    assert content == expected_content, f"The contents of {log_path} are incorrect. Expected:\n{expected_content}\nGot:\n{content}"