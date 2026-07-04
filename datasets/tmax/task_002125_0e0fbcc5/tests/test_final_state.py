# test_final_state.py

import os
import math
import pytest

def test_profile_results_generated_correctly():
    results_file = "/home/user/profile_results.txt"

    assert os.path.exists(results_file), f"The expected output file {results_file} was not generated."
    assert os.path.isfile(results_file), f"{results_file} is not a valid file."

    with open(results_file, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == 10, f"Expected exactly 10 lines in {results_file}, but found {len(lines)}."

    for i in range(10):
        expected_val = int(math.sqrt(i * 100))
        expected_line = f"Result {i}: {expected_val}"
        assert lines[i] == expected_line, f"Line {i+1} mismatch. Expected: '{expected_line}', but got: '{lines[i]}'."