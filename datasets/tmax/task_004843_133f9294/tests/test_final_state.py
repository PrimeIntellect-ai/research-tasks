# test_final_state.py

import os
import math

def test_final_state_exists():
    """Test that the final_state.txt file exists."""
    file_path = "/home/user/final_state.txt"
    assert os.path.exists(file_path), f"The file {file_path} is missing. Did you run the simulation and redirect output?"
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_final_state_content():
    """Test that the final_state.txt contains the correct numerical output."""
    file_path = "/home/user/final_state.txt"
    with open(file_path, "r") as f:
        content = f.read().strip()

    assert "NaN" not in content, "The output contains 'NaN', indicating the integrator diverged."
    assert "Step size too small" not in content, "The output indicates the step size became too small."

    parts = content.split()
    assert len(parts) == 5, f"Expected 5 numbers in the output, but found {len(parts)}."

    try:
        numbers = [float(p) for p in parts]
    except ValueError:
        assert False, "The output contains non-numeric values."

    total_mass = sum(numbers)
    assert math.isclose(total_mass, 10.0, rel_tol=1e-3), f"Total mass is not conserved. Sum is {total_mass}, expected ~10.0."

    # Check that the values are close to the expected equilibrium (around 2.0)
    for i, num in enumerate(numbers):
        assert 1.9 < num < 2.1, f"Value at index {i} ({num}) is too far from the expected equilibrium state."

def test_diffusion_c_fixed():
    """Test that diffusion.c contains the fixed step-size adaptation line."""
    file_path = "/home/user/diffusion.c"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()

    assert "sqrt(tol / err)" in content or "sqrt(tol/err)" in content, "The step-size adaptation logic does not appear to be fixed."

def test_binary_exists():
    """Test that the compiled binary exists."""
    binary_path = "/home/user/diffusion"
    assert os.path.exists(binary_path), f"The compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."