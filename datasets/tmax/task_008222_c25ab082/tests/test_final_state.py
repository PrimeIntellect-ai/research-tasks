# test_final_state.py
import os
import pytest

def test_script_exists():
    script_path = "/home/user/run_project.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_execution_log_exists_and_correct():
    log_path = "/home/user/execution_log.txt"
    assert os.path.isfile(log_path), f"The execution log {log_path} does not exist. Did you run your script?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ["20", "10"]
    assert lines == expected_lines, f"The execution log content is incorrect. Expected {expected_lines}, but got {lines}."