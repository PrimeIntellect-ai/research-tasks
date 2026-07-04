# test_final_state.py

import os
import subprocess
import pytest

def test_service_status_log_exists():
    log_path = "/home/user/service_status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

def test_service_status_log_content():
    log_path = "/home/user/service_status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Monitored mount: /home/user/data_mount with quota 1000" in content, \
        "Log does not contain the correct output for data_mount."
    assert "Monitored mount: /home/user/backup_mount with quota 500" in content, \
        "Log does not contain the correct output for backup_mount."
    assert "Storage monitor initialization complete." in content, \
        "Log does not indicate successful completion of the monitor daemon."

def test_setup_env_idempotent():
    script_path = "/home/user/setup_env.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Run the script. If it is idempotent, it should succeed even though directories exist.
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, \
        f"{script_path} failed when directories already exist. It is not idempotent.\nError: {result.stderr}"

def test_monitor_compiled_and_executable():
    binary_path = "/home/user/monitor"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."

def test_monitor_does_not_segfault():
    binary_path = "/home/user/monitor"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."

    # Run the compiled binary directly to ensure it doesn't crash on the fstab file
    result = subprocess.run([binary_path], capture_output=True, text=True)
    assert result.returncode == 0, \
        f"The monitor daemon crashed or exited with an error. Return code: {result.returncode}\nStderr: {result.stderr}"
    assert "Storage monitor initialization complete." in result.stdout, \
        "The monitor daemon did not print the completion message."