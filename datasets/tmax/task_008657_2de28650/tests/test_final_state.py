# test_final_state.py

import os
import pytest

def test_helper_binary_built():
    binary_path = "/home/user/sim_project/bin/helper"
    assert os.path.isfile(binary_path), f"Helper binary was not compiled at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"Helper binary at {binary_path} is not executable."

def test_input_dat_created_and_correct():
    input_path = "/home/user/sim_project/data/input.dat"
    assert os.path.isfile(input_path), f"Input file was not created at {input_path}."
    with open(input_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {input_path} is not a valid number: '{content}'.")

    assert val == 100.0, f"Expected input.dat to contain 100, but got {val}."

def test_output_result_created_and_correct():
    output_path = "/home/user/sim_project/output_result.txt"
    assert os.path.isfile(output_path), f"Output result file was not created at {output_path}. Did simulate.sh run successfully?"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {output_path} is not a valid number: '{content}'.")

    assert abs(val - 10.0) < 1e-9, f"Expected output_result.txt to contain a value extremely close to 10.0, but got {val}."

def test_simulate_sh_fixed():
    simulate_path = "/home/user/sim_project/simulate.sh"
    assert os.path.isfile(simulate_path), f"File {simulate_path} is missing."
    with open(simulate_path, 'r') as f:
        content = f.read()

    # Check if bc command was modified to use scale or -l
    assert "scale=" in content or "-l" in content, "simulate.sh does not appear to have been fixed to include precision in bc."