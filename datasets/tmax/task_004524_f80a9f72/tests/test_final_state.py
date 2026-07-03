# test_final_state.py

import os
import subprocess
import pytest
import re

def test_cpp_source_exists():
    path = "/home/user/filter_users.cpp"
    assert os.path.isfile(path), f"C++ source file {path} does not exist."

def test_cpp_executable_exists():
    path = "/home/user/filter_users"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_shell_script_exists_and_executable():
    path = "/home/user/check_users.sh"
    assert os.path.isfile(path), f"Shell script {path} does not exist."
    assert os.access(path, os.X_OK), f"Shell script {path} is not executable."

def test_cron_job_scheduled():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."

    cron_lines = result.stdout.strip().split("\n")
    found = False
    pattern = re.compile(r"^0\s+\*\s+\*\s+\*\s+\*\s+/home/user/check_users\.sh$")
    for line in cron_lines:
        if pattern.match(line.strip()):
            found = True
            break

    assert found, "Cron job for /home/user/check_users.sh at minute 0 (top of every hour) is missing or incorrectly formatted."

def test_check_users_script_behavior():
    # Remove log if it exists to ensure we get fresh output
    log_path = "/home/user/missing_users.log"
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run the shell script
    result = subprocess.run(["/home/user/check_users.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"Running /home/user/check_users.sh failed with error: {result.stderr}"

    assert os.path.isfile(log_path), f"Log file {log_path} was not created by the script."

    # Calculate expected missing users
    expected_users = []
    with open("/home/user/expected_users.txt", "r") as f:
        expected_users = [line.strip() for line in f if line.strip()]

    actual_users = []
    with open("/etc/passwd", "r") as f:
        for line in f:
            parts = line.split(":")
            if len(parts) >= 3:
                try:
                    uid = int(parts[2])
                    if uid >= 1000:
                        actual_users.append(parts[0])
                except ValueError:
                    pass

    missing_users = sorted(list(set(expected_users) - set(actual_users)))
    expected_log_lines = [f"Missing: {user}" for user in missing_users]

    with open(log_path, "r") as f:
        actual_log_lines = [line.strip() for line in f if line.strip()]

    assert actual_log_lines == expected_log_lines, (
        f"Contents of {log_path} do not match the expected missing users. "
        f"Expected: {expected_log_lines}, Got: {actual_log_lines}"
    )