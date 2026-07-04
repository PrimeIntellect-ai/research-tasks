# test_final_state.py

import os
from pathlib import Path

def test_bad_commit_sha_correct():
    expected_file = Path("/tmp/expected_bad_commit.txt")
    assert expected_file.exists(), "The expected bad commit file is missing from the environment."
    expected_sha = expected_file.read_text().strip()

    student_file = Path("/home/user/bad_commit_sha.txt")
    assert student_file.exists(), "The file /home/user/bad_commit_sha.txt does not exist."
    assert student_file.is_file(), "/home/user/bad_commit_sha.txt is not a file."

    student_sha = student_file.read_text().strip()
    assert student_sha == expected_sha, f"Incorrect bad commit SHA. Expected {expected_sha}, got {student_sha}."

def test_dropped_data_correct():
    student_file = Path("/home/user/dropped_data.txt")
    assert student_file.exists(), "The file /home/user/dropped_data.txt does not exist."
    assert student_file.is_file(), "/home/user/dropped_data.txt is not a file."

    student_data = student_file.read_text().strip()
    expected_data = "BETA 40"

    assert student_data == expected_data, f"Incorrect dropped data. Expected '{expected_data}', got '{student_data}'."