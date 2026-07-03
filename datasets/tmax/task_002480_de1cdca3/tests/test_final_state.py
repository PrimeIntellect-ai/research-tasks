# test_final_state.py

import os
import subprocess
import pytest

BUGGY_LINE = '10.0.0.5 [12/Nov/2023:03:14:15] "GET /weird path with spaces HTTP/1.1" 404 532'

def test_buggy_line_isolated():
    buggy_file = "/home/user/buggy_line.txt"
    assert os.path.isfile(buggy_file), f"The file {buggy_file} was not created."

    with open(buggy_file, "r") as f:
        content = f.read().strip()

    assert content == BUGGY_LINE, f"The isolated buggy line is incorrect. Expected: '{BUGGY_LINE}', but got: '{content}'"

def test_script_fixed():
    script_file = "/home/user/process_logs.py"
    logs_dir = "/home/user/logs"

    assert os.path.isfile(script_file), f"The script file {script_file} is missing."
    assert os.path.isdir(logs_dir), f"The directory {logs_dir} is missing."

    # Run the script against the logs directory
    result = subprocess.run(
        ["python3", script_file, logs_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"The script failed to execute successfully. Exit code: {result.returncode}\nStderr: {result.stderr}"

def test_original_logs_unmodified():
    log_file = "/home/user/logs/access_02.log"
    assert os.path.isfile(log_file), f"The log file {log_file} was deleted or moved."

    with open(log_file, "r") as f:
        content = f.read()

    assert BUGGY_LINE in content, f"The original log file {log_file} was modified and the buggy line is missing."