# test_final_state.py

import os
import re
import subprocess
import pytest

def test_automate_script_exists_and_executable():
    path = "/home/user/automate.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_legacy_config_output():
    config_path = "/home/user/.config/user_locale.conf"
    assert os.path.isfile(config_path), f"Configuration file {config_path} was not created."

    with open(config_path, "r") as f:
        content = f.read()

    assert "TZ=Etc/UTC" in content, f"Expected 'TZ=Etc/UTC' in {config_path}, but got:\n{content}"
    assert "LANG=en_US.UTF-8" in content, f"Expected 'LANG=en_US.UTF-8' in {config_path}, but got:\n{content}"

def test_check_storage_script_exists_and_executable():
    path = "/home/user/check_storage.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_storage_audit_log_contents():
    log_path = "/home/user/storage_audit.log"
    assert os.path.isfile(log_path), f"Audit log file {log_path} was not created."

    # Calculate expected size using du -sk
    target_dir = "/home/user/secure_storage"
    try:
        du_output = subprocess.check_output(["du", "-sk", target_dir], text=True).strip()
        size_kb = int(du_output.split()[0])
    except Exception as e:
        pytest.fail(f"Could not calculate size of {target_dir}: {e}")

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"Audit log {log_path} is empty."

    last_line = lines[-1]

    if size_kb >= 5000:
        expected_line = f"ALERT: secure_storage is {size_kb}KB"
    else:
        expected_line = f"OK: secure_storage is {size_kb}KB"

    assert last_line == expected_line, f"Expected log line '{expected_line}', but got '{last_line}'"