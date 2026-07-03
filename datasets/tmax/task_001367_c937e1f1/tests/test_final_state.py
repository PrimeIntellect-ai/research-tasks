# test_final_state.py

import os
import pytest

def test_solve_script_exists():
    """Test that the solve.py script exists."""
    solve_script = "/home/user/solve.py"
    assert os.path.isfile(solve_script), f"The script {solve_script} is missing. Did you create it?"

def test_optimized_mu_file_exists():
    """Test that the optimized_mu.txt file exists."""
    output_txt = "/home/user/optimized_mu.txt"
    assert os.path.isfile(output_txt), f"The output file {output_txt} is missing. Did you run your script and save the output?"

def test_optimized_mu_value():
    """Test that the optimized mu value is correct."""
    output_txt = "/home/user/optimized_mu.txt"
    with open(output_txt, 'r') as f:
        val = f.read().strip()

    expected_val = "500.00"
    assert val == expected_val, f"Incorrect mu value: '{val}'. Expected '{expected_val}'."