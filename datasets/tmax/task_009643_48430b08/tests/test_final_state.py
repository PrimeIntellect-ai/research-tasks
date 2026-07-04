# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_identified():
    student_file = "/home/user/bad_commit.txt"
    truth_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(student_file), f"File {student_file} does not exist. You must write the bad commit hash to this file."
    assert os.path.isfile(truth_file), f"Truth file {truth_file} is missing. The environment is broken."

    with open(student_file, "r") as f:
        student_commit = f.read().strip()

    with open(truth_file, "r") as f:
        truth_commit = f.read().strip()

    assert student_commit == truth_commit, f"The commit hash in {student_file} is incorrect. Expected {truth_commit}, got {student_commit}."

def test_fixed_script_exists_and_executable():
    fixed_script = "/home/user/parse_trace_fixed.sh"
    assert os.path.isfile(fixed_script), f"Fixed script {fixed_script} does not exist."
    assert os.access(fixed_script, os.X_OK), f"Fixed script {fixed_script} is not executable."

def test_fixed_script_output():
    fixed_script = "/home/user/parse_trace_fixed.sh"
    trace_file = "/home/user/edge_case_trace.log"

    assert os.path.isfile(fixed_script), f"Fixed script {fixed_script} does not exist."
    assert os.path.isfile(trace_file), f"Trace file {trace_file} does not exist."

    expected_output = [
        "1.1.1.1",
        "10.0.0.5",
        "172.16.254.1",
        "192.168.1.50",
        "8.8.8.8"
    ]

    try:
        result = subprocess.run(
            [fixed_script, trace_file],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing {fixed_script} failed with return code {e.returncode}.\nStderr: {e.stderr}")

    actual_output = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]

    assert actual_output == expected_output, (
        f"The output of {fixed_script} is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_output)}\n\n"
        f"Got:\n{chr(10).join(actual_output)}"
    )