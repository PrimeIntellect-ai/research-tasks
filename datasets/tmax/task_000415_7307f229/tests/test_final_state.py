# test_final_state.py

import os
import subprocess
import pytest

def test_netmon_v1_killed():
    """Verify that no processes named netmon_v1 are running."""
    try:
        output = subprocess.check_output(["pgrep", "netmon_v1"]).decode("utf-8").strip()
        # If pgrep returns output, processes are still running
        assert not output, f"netmon_v1 processes are still running: {output}"
    except subprocess.CalledProcessError:
        # pgrep returns non-zero exit code if no processes match, which is what we want
        pass

def test_netmon_v2_compiled():
    """Verify that netmon_v2 is compiled in /home/user/."""
    path = "/home/user/netmon_v2"
    assert os.path.isfile(path), f"Compiled binary {path} is missing."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_stage_alpha_deployment():
    """Verify deployment in /home/user/stage_alpha."""
    target_dir = "/home/user/stage_alpha"
    assert os.path.isdir(target_dir), f"Directory {target_dir} was not created."

    binary_path = os.path.join(target_dir, "netmon_v2")
    assert os.path.isfile(binary_path), f"Binary {binary_path} was not copied."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

    log_path = os.path.join(target_dir, "monitor.log")
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        log_content = f.read().strip().splitlines()

    expected_lines = [
        "[netadmin] 192.168.1.10 10.0.0.5",
        "[dbdaemon] 192.168.1.12 10.0.0.7",
        "[UNKNOWN] 192.168.1.13 10.0.0.8"
    ]

    assert len(log_content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(log_content)}."
    for expected in expected_lines:
        assert expected in log_content, f"Expected line '{expected}' not found in {log_path}."

def test_stage_beta_deployment():
    """Verify deployment in /home/user/stage_beta."""
    target_dir = "/home/user/stage_beta"
    assert os.path.isdir(target_dir), f"Directory {target_dir} was not created."

    binary_path = os.path.join(target_dir, "netmon_v2")
    assert os.path.isfile(binary_path), f"Binary {binary_path} was not copied."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

    log_path = os.path.join(target_dir, "monitor.log")
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        log_content = f.read().strip().splitlines()

    expected_lines = [
        "[netadmin] 192.168.1.10 10.0.0.5",
        "[dbdaemon] 192.168.1.12 10.0.0.7",
        "[UNKNOWN] 192.168.1.13 10.0.0.8"
    ]

    assert len(log_content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(log_content)}."
    for expected in expected_lines:
        assert expected in log_content, f"Expected line '{expected}' not found in {log_path}."