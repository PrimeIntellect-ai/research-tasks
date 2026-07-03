# test_final_state.py

import os
import stat
import pytest

def test_process_sh_exists_and_executable():
    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"{script_path} is not executable"

def test_process_sh_contains_flock():
    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"

    with open(script_path, "r") as f:
        content = f.read()

    assert "flock" in content, f"{script_path} does not use 'flock' as required"

def test_consolidated_log_exists_and_content():
    log_path = "/home/user/project_logs/consolidated.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did the script run?"

    expected_lines = [
        "LogEntryA: Start Job 123",
        "LogEntryB: Processing Data...",
        "LogEntryC: End Job 123"
    ]

    with open(log_path, "r") as f:
        actual_lines = f.read().splitlines()

    assert actual_lines == expected_lines, \
        f"Contents of {log_path} do not match the expected consolidated log entries. Got: {actual_lines}"