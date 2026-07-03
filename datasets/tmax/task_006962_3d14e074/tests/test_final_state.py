# test_final_state.py

import os
import pytest

def test_symlink_app_current():
    """Test that /home/user/app_current is a symlink pointing to /home/user/releases/v2."""
    symlink_path = "/home/user/app_current"
    target_path = "/home/user/releases/v2"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.readlink(symlink_path) == target_path, f"{symlink_path} does not point to {target_path}."

def test_logs_directory_exists():
    """Test that /home/user/logs directory exists."""
    logs_dir = "/home/user/logs"
    assert os.path.isdir(logs_dir), f"Directory {logs_dir} is missing."

def test_start_proxy_script():
    """Test that /home/user/start_proxy.sh exists, is executable, and contains correct socat configurations."""
    script_path = "/home/user/start_proxy.sh"

    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "socat" in content, f"{script_path} does not contain 'socat'."
    assert "8080" in content, f"{script_path} does not contain port '8080'."
    assert "8081" in content, f"{script_path} does not contain port '8081'."

def test_start_worker_script():
    """Test that /home/user/start_worker.sh exists, is executable, and contains correct environment variables."""
    script_path = "/home/user/start_worker.sh"

    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "Europe/Berlin" in content, f"{script_path} does not set TZ to 'Europe/Berlin'."
    assert "en_US.UTF-8" in content, f"{script_path} does not set LC_ALL to 'en_US.UTF-8'."

def test_worker_output_log():
    """Test that /home/user/logs/worker_output.log exists and contains the correct output."""
    log_path = "/home/user/logs/worker_output.log"

    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did the worker script run successfully?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "Version: v2" in content, "Log file does not contain 'Version: v2'."
    assert "TZ: Europe/Berlin" in content, "Log file does not contain 'TZ: Europe/Berlin'."
    assert "LC_ALL: en_US.UTF-8" in content, "Log file does not contain 'LC_ALL: en_US.UTF-8'."
    assert "CWD: /home/user/logs" in content, "Log file does not contain 'CWD: /home/user/logs'. Working directory was not changed correctly."