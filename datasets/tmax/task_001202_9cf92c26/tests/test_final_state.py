# test_final_state.py

import os
import re
import math
import pytest

def test_files_exist():
    """Verify that all required files exist."""
    required_files = [
        "/home/user/poisson1d.c",
        "/home/user/pipeline.sh",
        "/home/user/plot.py",
        "/home/user/convergence.log",
        "/home/user/solution_159.dat",
        "/home/user/convergence.png",
        "/home/user/solution.png"
    ]
    for file_path in required_files:
        assert os.path.exists(file_path), f"Required file {file_path} is missing."

def test_pipeline_is_executable():
    """Verify that pipeline.sh has execution permissions."""
    assert os.access("/home/user/pipeline.sh", os.X_OK), "/home/user/pipeline.sh is not executable."

def test_convergence_log():
    """Verify the contents of convergence.log match the expected output."""
    log_path = "/home/user/convergence.log"
    assert os.path.exists(log_path), f"{log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_Ns = [9, 19, 39, 79, 159]
    assert len(lines) == len(expected_Ns), f"Expected {len(expected_Ns)} lines in convergence.log, found {len(lines)}."

    for i, N in enumerate(expected_Ns):
        h = 1.0 / (N + 1)
        # Exact L2 error = (1/sqrt(2)) * | (pi^2 * h^2)/(2 * (1 - cos(pi * h))) - 1 |
        expected_error = (1.0 / math.sqrt(2.0)) * abs((math.pi**2 * h**2) / (2.0 * (1.0 - math.cos(math.pi * h))) - 1.0)

        line = lines[i]
        match = re.match(r"^N=(\d+),\s*h=([0-9.]+),\s*error=([0-9.]+)$", line)
        assert match, f"Line {i+1} in convergence.log is incorrectly formatted: '{line}'"

        parsed_N = int(match.group(1))
        parsed_h = float(match.group(2))
        parsed_error = float(match.group(3))

        assert parsed_N == N, f"Expected N={N} on line {i+1}, found N={parsed_N}."
        assert math.isclose(parsed_h, h, rel_tol=1e-4), f"Expected h={h:.6f} for N={N}, found {parsed_h}."
        assert math.isclose(parsed_error, expected_error, abs_tol=5e-6), f"Expected error near {expected_error:.6f} for N={N}, found {parsed_error}."

def test_solution_dat_files():
    """Verify that the solution data files are generated."""
    expected_Ns = [9, 19, 39, 79, 159]
    for N in expected_Ns:
        file_path = f"/home/user/solution_{N}.dat"
        assert os.path.exists(file_path), f"Data file {file_path} is missing."