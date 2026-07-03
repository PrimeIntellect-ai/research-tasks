# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
RUNNER_SCRIPT = os.path.join(PROJECT_DIR, "ci_runner.sh")
REPORT_FILE = os.path.join(PROJECT_DIR, "ci_report.txt")

def test_runner_script_exists_and_executable():
    assert os.path.isfile(RUNNER_SCRIPT), f"The script {RUNNER_SCRIPT} does not exist."
    assert os.access(RUNNER_SCRIPT, os.X_OK), f"The script {RUNNER_SCRIPT} is not executable."

def test_runner_script_no_args_exit_code():
    # Running the script without arguments should exit with status code 1
    result = subprocess.run([RUNNER_SCRIPT], capture_output=True)
    assert result.returncode == 1, f"Expected exit code 1 when no arguments are provided, got {result.returncode}."

def test_runner_script_invalid_executable_exit_code():
    # Running the script with a non-executable file should exit with status code 1
    dummy_file = os.path.join(PROJECT_DIR, "dummy.txt")
    with open(dummy_file, "w") as f:
        f.write("test")

    result = subprocess.run([RUNNER_SCRIPT, dummy_file], capture_output=True)
    assert result.returncode == 1, f"Expected exit code 1 when argument is not executable, got {result.returncode}."

    os.remove(dummy_file)

def test_ci_report_content():
    assert os.path.isfile(REPORT_FILE), f"The report file {REPORT_FILE} does not exist."

    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {REPORT_FILE}, got {len(lines)}."
    assert lines[0] == "LINKING: SUCCESS", f"Expected first line to be 'LINKING: SUCCESS', got '{lines[0]}'."
    assert lines[1] == "LEAKED_BYTES: 128", f"Expected second line to be 'LEAKED_BYTES: 128', got '{lines[1]}'."