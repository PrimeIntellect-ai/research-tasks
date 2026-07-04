# test_final_state.py

import os
import pytest

def test_solution_file_exists():
    """Test that the solution.txt file exists."""
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"Expected solution file not found at {solution_path}"

def test_solution_content():
    """Test that the solution.txt contains the correct converged value."""
    solution_path = "/home/user/solution.txt"
    with open(solution_path, "r") as f:
        content = f.read().strip()

    assert content == "2.25", f"Expected solution to be '2.25', but got '{content}'"

def test_script_modified_correctly():
    """Test that the Go script still has the required constants but added clipping logic."""
    script_path = "/home/user/test_stability.go"
    assert os.path.isfile(script_path), f"Go script missing at {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    # Check that initial conditions were not changed
    assert "x := 4.0" in content or "x = 4.0" in content, "Initial x value was changed."
    assert "lr := 0.1" in content or "lr = 0.1" in content, "Learning rate was changed."
    assert "iterations := 1000" in content or "iterations = 1000" in content, "Iterations count was changed."

    # Check that gradient clipping logic is likely present
    # Could be math.Max/math.Min, or if/else statements with 5.0 and -5.0
    has_clipping = ("5.0" in content and "-5.0" in content) or ("5" in content and "-5" in content)
    assert has_clipping, "Could not find gradient clipping logic (checking for bounds 5.0 and -5.0) in the script."