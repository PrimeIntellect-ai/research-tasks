# test_final_state.py

import os
import subprocess

def test_script_exists_and_executable():
    script_path = "/home/user/find_deadlocks.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_deadlocks_log_exists():
    log_path = "/home/user/deadlocks.log"
    assert os.path.exists(log_path), f"The log file {log_path} does not exist. Did you run the script?"
    assert os.path.isfile(log_path), f"The path {log_path} is not a file."

def test_deadlocks_log_content():
    log_path = "/home/user/deadlocks.log"
    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_lines = ["T001,T002", "T005,T007"]
    actual_lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {log_path} do not match expected output for 2023-10-01.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {actual_lines}"
    )

def test_script_parameterization():
    script_path = "/home/user/find_deadlocks.sh"
    log_path = "/home/user/deadlocks.log"

    # Run the script for another date to test parameterization
    try:
        subprocess.run([script_path, "2023-10-02"], check=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to execute {script_path} with argument '2023-10-02': {e}"

    assert os.path.exists(log_path), f"The log file {log_path} was not created after running the script."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_lines = ["T009,T010"]
    actual_lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert actual_lines == expected_lines, (
        f"Script did not correctly process the date parameter '2023-10-02'.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {actual_lines}"
    )