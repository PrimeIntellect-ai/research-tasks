# test_final_state.py

import os
import re
import pytest

def test_task_done_file():
    """Verify that the task_done.txt file exists."""
    path = "/home/user/task_done.txt"
    assert os.path.exists(path), f"File {path} does not exist. Did you forget to create it?"
    assert os.path.isfile(path), f"Path {path} is not a regular file."

def test_app_metrics_log():
    """Verify that the app_metrics.log exists and contains the correct payload."""
    path = "/home/user/app_metrics.log"
    assert os.path.exists(path), f"Log file {path} does not exist. The end-to-end test may not have executed correctly."

    with open(path, "r") as f:
        content = f.read()

    assert "TEST_RESTORE_METRIC: SUCCESS_42" in content, (
        f"The expected payload was not found in {path}. "
        "Check if port forwarding and the daemon were working correctly."
    )

def test_metrics_daemon_executable():
    """Verify that the metrics_daemon was compiled and is an ELF executable."""
    exe_path = "/home/user/restore/metrics_daemon"
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    with open(exe_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File {exe_path} is not a valid ELF binary."

def test_logrotate_config():
    """Verify that the logrotate configuration contains the required directives."""
    path = "/home/user/logrotate.conf"
    assert os.path.exists(path), f"Logrotate configuration {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "/home/user/app_metrics.log" in content, f"Logrotate config must target /home/user/app_metrics.log"

    # Check for required directives
    assert re.search(r'\bhourly\b', content), "Directive 'hourly' is missing from logrotate config."
    assert re.search(r'\brotate\s+5\b', content), "Directive 'rotate 5' is missing from logrotate config."
    assert re.search(r'\bcompress\b', content), "Directive 'compress' is missing from logrotate config."
    assert re.search(r'\bmissingok\b', content), "Directive 'missingok' is missing from logrotate config."

def test_metrics_daemon_source_fixed():
    """Verify that the C++ source code was updated with the new socket path."""
    src_path = "/home/user/restore/metrics_daemon.cpp"
    assert os.path.exists(src_path), f"Source file {src_path} does not exist."

    with open(src_path, "r") as f:
        content = f.read()

    assert "/home/user/app.sock" in content, (
        f"The new socket path '/home/user/app.sock' was not found in {src_path}."
    )
    assert "/home/user/old.sock" not in content, (
        f"The old socket path '/home/user/old.sock' is still present in {src_path}."
    )