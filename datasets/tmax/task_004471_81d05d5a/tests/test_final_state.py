# test_final_state.py

import os
import pytest

def test_final_state():
    solve_script_path = "/home/user/solve.py"
    resolution_path = "/home/user/resolution.txt"

    # Check if solve.py exists
    assert os.path.isfile(solve_script_path), f"File missing: {solve_script_path}. You must write the solution script here."

    # Check if resolution.txt exists
    assert os.path.isfile(resolution_path), f"File missing: {resolution_path}. The script must output the result here."

    # Check the contents of resolution.txt
    with open(resolution_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_value = "7.62079e-17"
    assert content == expected_value, (
        f"Incorrect value in {resolution_path}. "
        f"Expected '{expected_value}', but got '{content}'."
    )