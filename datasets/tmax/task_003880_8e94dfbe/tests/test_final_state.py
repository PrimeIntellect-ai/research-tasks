# test_final_state.py
import os
import stat
import pytest

def test_alerts_log_content():
    path = "/home/user/alerts.log"
    assert os.path.isfile(path), f"Missing file: {path}"

    expected_lines = [
        "[ALERT] Value 90 exceeds threshold",
        "[ALERT] Value 95 exceeds threshold",
        "[ALERT] Value 100 exceeds threshold",
        "[ALERT] Value 86 exceeds threshold"
    ]

    with open(path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, f"Content of {path} does not match the expected output. Got: {content}"

def test_bashrc_contains_export():
    path = "/home/user/.bashrc"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "export ALERT_THRESHOLD=85" in content, f"{path} does not contain 'export ALERT_THRESHOLD=85'"

def test_worker_binary_executable():
    path = "/home/user/worker"
    assert os.path.isfile(path), f"Missing compiled binary: {path}"

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {path} is not executable"

def test_run_monitor_sh_executable():
    path = "/home/user/run_monitor.sh"
    assert os.path.isfile(path), f"Missing script: {path}"

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {path} is not executable"

def test_worker_c_uses_getenv():
    path = "/home/user/worker.c"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "getenv" in content, f"{path} does not appear to use getenv() to read the environment variable."