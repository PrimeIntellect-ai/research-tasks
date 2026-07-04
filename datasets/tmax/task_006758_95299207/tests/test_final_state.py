# test_final_state.py

import os
import subprocess
import pytest

def test_bug_commit_txt_matches_expected():
    student_file = "/home/user/bug_commit.txt"
    expected_file = "/tmp/expected_bug_commit.txt"

    assert os.path.isfile(student_file), f"File {student_file} does not exist. Did you save the commit hash?"
    assert os.path.isfile(expected_file), f"Expected file {expected_file} is missing."

    with open(student_file, "r") as f:
        student_hash = f.read().strip()

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    assert student_hash == expected_hash, f"The commit hash in {student_file} ({student_hash}) does not match the expected bug commit hash."

def test_calc_sh_correct_for_negative_numbers():
    script_path = "/home/user/math_parser/calc.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

    result = subprocess.run([script_path, "MUL", "-5", "-6"], capture_output=True, text=True)

    assert result.returncode == 0, f"Expected return code 0 for valid input, got {result.returncode}"
    assert result.stdout.strip() == "30", f"Expected output '30' for 'MUL -5 -6', got '{result.stdout.strip()}'"

def test_calc_sh_rejects_invalid_input():
    script_path = "/home/user/math_parser/calc.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    result = subprocess.run([script_path, "ADD", "5", "a"], capture_output=True, text=True)

    assert result.returncode != 0, f"Expected non-zero return code for invalid input, got {result.returncode}"
    assert result.stdout.strip() == "Error", f"Expected output 'Error' for invalid input, got '{result.stdout.strip()}'"