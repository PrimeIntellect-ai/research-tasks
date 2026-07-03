# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_results_file():
    results_file = "/home/user/results.txt"
    assert os.path.exists(results_file), "results.txt not found"

    with open(results_file, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    assert len(lines) >= 2, "results.txt needs at least 2 lines"

    try:
        w_A = float(lines[0])
        diff = float(lines[1])
    except ValueError:
        pytest.fail("results.txt contains non-numeric values")

    assert 0.29 <= w_A <= 0.31, f"Incorrect weight w_A: {w_A}. Expected 0.3"
    assert 0.0 <= diff <= 0.02, f"Monte Carlo difference too large or invalid: {diff}"

def test_simulate_script_exists_and_executable():
    script_path = "/home/user/simulate.sh"
    assert os.path.exists(script_path), "simulate.sh not found"
    assert os.access(script_path, os.X_OK), "simulate.sh is not executable"

def test_simulate_script_execution():
    script_path = "/home/user/simulate.sh"
    # Run the script with the correct w_A (0.3)
    try:
        result = subprocess.run([script_path, "0.3"], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"simulate.sh failed with return code {result.returncode}"
        output = result.stdout.strip()

        # Output should be a float
        simulated_gc = float(output)

        # If w_A is 0.3, expected GC is 0.40. Allow some variance.
        assert 0.35 <= simulated_gc <= 0.45, f"Simulated GC-content {simulated_gc} is out of expected range for w_A=0.3"
    except Exception as e:
        pytest.fail(f"Failed to execute simulate.sh or parse its output: {e}")