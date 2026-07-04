# test_final_state.py
import os
import pytest

REPO_DIR = "/home/user/solver_repo"
REQ_FILE = os.path.join(REPO_DIR, "requirements.txt")
SOLVER_FILE = os.path.join(REPO_DIR, "solver.py")
SOLUTION_FILE = "/home/user/solution.txt"

def test_requirements_fixed():
    assert os.path.isfile(REQ_FILE), f"File {REQ_FILE} does not exist."
    with open(REQ_FILE, "r") as f:
        content = f.read()
    assert "scipy" in content, "scipy dependency not fixed in requirements.txt."
    assert "scipppy" not in content, "Typo 'scipppy' still present in requirements.txt."

def test_solution_file_exists_and_correct():
    assert os.path.isfile(SOLUTION_FILE), f"Solution file {SOLUTION_FILE} does not exist."
    with open(SOLUTION_FILE, "r") as f:
        content = f.read().strip()

    # The expected root for x^3 - 2x + 2 = 0 is approximately -1.76929235
    # Rounded to 6 decimal places is -1.769292
    assert content == "-1.769292", f"Expected solution to be '-1.769292', but got '{content}'."