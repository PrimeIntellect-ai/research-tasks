# test_final_state.py

import os
import re
import pytest

def test_solution_file_exists():
    assert os.path.isfile("/home/user/solution.txt"), "/home/user/solution.txt does not exist. Did you create it?"

def test_solution_content_matches_expected():
    solution_path = "/home/user/solution.txt"
    expected_path = "/tmp/expected_solution.txt"

    assert os.path.isfile(expected_path), "Expected solution file is missing from the environment."
    assert os.path.isfile(solution_path), "Solution file is missing."

    with open(solution_path, "r") as f:
        student_content = f.read().strip()

    with open(expected_path, "r") as f:
        expected_content = f.read().strip()

    # Parse expected values
    expected_commit = None
    expected_function = None
    for line in expected_content.splitlines():
        if line.startswith("Commit:"):
            expected_commit = line.split(":", 1)[1].strip()
        elif line.startswith("Function:"):
            expected_function = line.split(":", 1)[1].strip()

    assert expected_commit, "Could not parse expected commit"
    assert expected_function, "Could not parse expected function"

    # Parse student values
    student_commit = None
    student_function = None
    for line in student_content.splitlines():
        if line.startswith("Commit:"):
            student_commit = line.split(":", 1)[1].strip()
        elif line.startswith("Function:"):
            student_function = line.split(":", 1)[1].strip()

    assert student_commit is not None, "Could not find 'Commit: <hash>' in /home/user/solution.txt"
    assert student_function is not None, "Could not find 'Function: <name>' in /home/user/solution.txt"

    assert student_commit == expected_commit, f"Incorrect commit hash. Expected {expected_commit}, got {student_commit}"
    assert student_function == expected_function, f"Incorrect function name. Expected {expected_function}, got {student_function}"