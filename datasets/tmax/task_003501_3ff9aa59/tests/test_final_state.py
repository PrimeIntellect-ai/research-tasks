# test_final_state.py

import os
import pytest

def test_solution_file_content():
    """Verify that the solution file contains the correct final sequence number."""
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"Solution file {solution_path} is missing."

    with open(solution_path, "r") as f:
        content = f.read().strip()

    expected_value = "8000000000000001000"
    assert content == expected_value, f"Expected {solution_path} to contain exactly '{expected_value}', but got '{content}'."

def test_datagen_script_modifications():
    """Verify that datagen.sh has been modified to handle overflows."""
    script_path = "/home/user/datagen.sh"
    assert os.path.isfile(script_path), f"Script file {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "OVERFLOW_ERROR" in content, f"The script {script_path} does not contain the required 'OVERFLOW_ERROR' string."
    assert "break" in content, f"The script {script_path} does not contain a 'break' statement to exit the loop."