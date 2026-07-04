# test_final_state.py

import os
import pytest

SOLUTION_PATH = "/home/user/solution.txt"
EXPECTED_OUTPUT = "PATH: ROOT->A->B->LEAF | DURATION: 35"

def test_solution_file_exists():
    assert os.path.isfile(SOLUTION_PATH), f"Solution file not found at {SOLUTION_PATH}"

def test_solution_content():
    with open(SOLUTION_PATH, "r") as f:
        content = f.read().strip()

    assert content == EXPECTED_OUTPUT, f"Expected '{EXPECTED_OUTPUT}', but got '{content}'"