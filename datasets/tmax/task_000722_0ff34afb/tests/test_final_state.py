# test_final_state.py

import os
import subprocess
import tempfile

def test_bad_commit_txt():
    expected_file = "/home/user/.expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(actual_file), f"{actual_file} does not exist. You must write the bad commit SHA-1 to this file."

    with open(expected_file, "r") as f:
        expected_commit = f.read().strip()

    with open(actual_file, "r") as f:
        actual_commit = f.read().strip()

    assert actual_commit == expected_commit, f"The commit hash in {actual_file} is incorrect. Expected {expected_commit}, but got {actual_commit}."

def test_fixed_script_exists_and_executable():
    script_path = "/home/user/fixed_process_logs.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_fixed_script_output_test_log():
    script_path = "/home/user/fixed_process_logs.sh"
    log_path = "/home/user/test_log.txt"

    result = subprocess.run([script_path, log_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {script_path} failed with return code {result.returncode}."

    output = result.stdout.strip()
    expected_output = "ERROR: 1\nINFO: 2\nWARN: 1"

    # Sort both to be robust against output ordering, though the script usually sorts
    actual_lines = sorted(output.splitlines())
    expected_lines = sorted(expected_output.splitlines())

    assert actual_lines == expected_lines, f"Output from {script_path} on {log_path} is incorrect.\nExpected:\n{expected_output}\nGot:\n{output}"

def test_fixed_script_output_edge_case():
    script_path = "/home/user/fixed_process_logs.sh"

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        tmp.write("[2023-10-01 12:04:00] [DEBUG] [INFO] WARN ERROR\n")
        tmp_path = tmp.name

    try:
        result = subprocess.run([script_path, tmp_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Running {script_path} on edge case failed."

        output = result.stdout.strip()
        expected_output = "DEBUG: 1"

        assert output == expected_output, f"Output from {script_path} on edge case is incorrect.\nExpected:\n{expected_output}\nGot:\n{output}"
    finally:
        os.remove(tmp_path)