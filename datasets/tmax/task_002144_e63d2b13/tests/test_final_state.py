# test_final_state.py

import os
import statistics
import pytest

SOLUTION_FILE = "/home/user/pipeline/solution.txt"

def test_solution_file_exists():
    assert os.path.isfile(SOLUTION_FILE), f"Solution file {SOLUTION_FILE} does not exist. Did you save the output to the correct path?"

def test_solution_content():
    # Recompute the expected value based on the deterministic LCG
    seed = 4004
    data = []
    for i in range(1000):
        seed = (seed * 1103515245 + 12345) & 0x7fffffff
        rand_val = seed / 2147483647.0
        data.append(100000000.0 + rand_val * 0.001)

    ans = statistics.pstdev(data)
    expected_content = f"StreamID: 4004, StdDev: {ans:.6f}"

    with open(SOLUTION_FILE, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Content of {SOLUTION_FILE} is incorrect. Expected '{expected_content}', but got '{actual_content}'."