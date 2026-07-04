# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_identified_correctly():
    expected_path = "/tmp/expected_bad_commit.txt"
    student_path = "/home/user/bad_commit.txt"

    assert os.path.isfile(expected_path), f"Truth file {expected_path} is missing."
    assert os.path.isfile(student_path), f"Student output file {student_path} is missing."

    with open(expected_path, "r") as f:
        expected_commit = f.read().strip()

    with open(student_path, "r") as f:
        student_commit = f.read().strip()

    assert student_commit == expected_commit, (
        f"Incorrect bad commit hash. Expected '{expected_commit}', but got '{student_commit}'."
    )

def test_final_sum_is_correct():
    student_path = "/home/user/final_sum.txt"
    assert os.path.isfile(student_path), f"Student output file {student_path} is missing."

    with open(student_path, "r") as f:
        student_sum = f.read().strip()

    assert student_sum == "150", (
        f"Incorrect final sum. Expected '150', but got '{student_sum}'."
    )

def test_aggregate_script_fixes():
    script_path = "/home/user/math_processor/aggregate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Execute the script. It might optionally take the data directory as an argument, 
    # though the original hardcoded it. We try without args first, then with args if it fails.
    result = subprocess.run(
        [script_path], 
        cwd="/home/user/math_processor", 
        capture_output=True, 
        text=True
    )

    if result.returncode != 0 or "150" not in result.stdout:
        result = subprocess.run(
            [script_path, "/home/user/data_dir"], 
            cwd="/home/user/math_processor", 
            capture_output=True, 
            text=True
        )

    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"
    assert "150" in result.stdout.strip().split("\n"), (
        f"Script did not output the correct sum (150). Output was: {result.stdout}"
    )