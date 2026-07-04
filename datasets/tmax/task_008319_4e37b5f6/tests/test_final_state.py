# test_final_state.py

import os
import pytest

def test_solution_txt():
    solution_path = "/home/user/solution.txt"
    assert os.path.exists(solution_path), f"File {solution_path} is missing."
    assert os.path.isfile(solution_path), f"{solution_path} is not a file."

    with open(solution_path, "r") as f:
        content = f.read().strip()

    assert content == "0.0141", f"Expected solution.txt to contain '0.0141', but got '{content}'"

def test_main_go_modified():
    go_path = "/home/user/statscalc/main.go"
    assert os.path.exists(go_path), f"File {go_path} is missing."

    with open(go_path, "r") as f:
        content = f.read()

    # Check for Welford's algorithm characteristics and task requirements
    assert "float64" in content, "The Go code must use float64 internally for precision."
    assert "panic" in content, "The Go code must contain a panic statement to validate variance."

    # Check that the naive implementation was removed or modified
    # The original file had "sumSq += f * f"
    # It's possible the user kept it in a comment, but we should at least see Welford's logic
    # Welford's typically involves calculating a delta
    assert "float32" in content, "The Go code should still decode values into float32 initially."