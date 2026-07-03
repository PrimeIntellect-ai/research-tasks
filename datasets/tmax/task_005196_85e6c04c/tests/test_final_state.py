# test_final_state.py

import os
import re
import math
import pytest

def test_clean_obs_txt_exists_and_correct():
    path = "/home/user/clean_obs.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you save the cleaned data?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected 5 lines of data in {path}, got {len(lines)}."

    # Verify the sorted values
    expected_lines = [
        "0.1 0.11",
        "0.2 0.55",
        "0.5 0.88",
        "0.8 0.22",
        "0.9 0.33"
    ]

    for i, expected in enumerate(expected_lines):
        # We allow multiple spaces or slightly different formatting as long as values match
        parts = lines[i].split()
        assert len(parts) == 2, f"Line {i+1} in {path} does not have exactly 2 columns."

        try:
            x_val = float(parts[0])
            y_val = float(parts[1])
            exp_x, exp_y = map(float, expected.split())
            assert math.isclose(x_val, exp_x, rel_tol=1e-5), f"Line {i+1} x-value mismatch: got {x_val}, expected {exp_x}"
            assert math.isclose(y_val, exp_y, rel_tol=1e-5), f"Line {i+1} y-value mismatch: got {y_val}, expected {exp_y}"
        except ValueError:
            pytest.fail(f"Could not parse floats from line {i+1} in {path}: '{lines[i]}'")

def test_solver_cpp_modified():
    path = "/home/user/simulation/solver.cpp"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check for regularization addition: A[i][i] += 1e-5 or similar
    # We'll use a regex to look for A[something][something] and 1e-5
    # The student might write A[i][i] = A[i][i] + 1e-5;
    assert "1e-5" in content or "0.00001" in content, "Could not find the regularization term '1e-5' in solver.cpp."

    # Ensure it looks like A[...][...] is being modified
    assert re.search(r'A\[[^\]]+\]\[[^\]]+\]\s*\+?=\s*(.*1e-5|.*0\.00001)', content) or \
           re.search(r'A\[[^\]]+\]\[[^\]]+\]\s*=\s*A\[[^\]]+\]\[[^\]]+\]\s*\+\s*(1e-5|0\.00001)', content), \
           "Could not find the exact logic adding 1e-5 to the matrix A in solver.cpp."

def test_compiled_executable_exists():
    path = "/home/user/simulation/mcmc_sim"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the code?"
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_posterior_mean_exists_and_valid():
    path = "/home/user/posterior_mean.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did the simulation run successfully?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content, f"File {path} is empty."

    try:
        val = float(content)
        assert math.isfinite(val), f"Posterior mean in {path} is not finite (got {val})."
        assert val != 0.0, "Posterior mean is exactly 0.0, which is unexpected for this simulation."
    except ValueError:
        pytest.fail(f"Could not parse a valid float from {path}. Content: '{content}'")