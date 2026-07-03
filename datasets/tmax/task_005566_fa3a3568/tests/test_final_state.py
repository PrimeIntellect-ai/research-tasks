# test_final_state.py

import os
import subprocess
import math
import pytest

def test_failure_line():
    failure_file = "/home/user/failure_line.txt"
    assert os.path.exists(failure_file), f"{failure_file} does not exist."

    # Run original script to find the expected failure line
    try:
        out = subprocess.check_output(["/home/user/calc_variance.sh", "/home/user/mem_stats.log"], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Original script failed to run: {e}")

    expected_failure_line = None
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            n = int(parts[0])
            var = float(parts[1])
            if var < 0:
                expected_failure_line = n
                break

    assert expected_failure_line is not None, "Original script did not produce a negative variance."

    with open(failure_file, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"{failure_file} must contain only the line number."
    assert int(content) == expected_failure_line, f"Expected failure line {expected_failure_line}, but got {content}."

def test_fixed_calc_variance():
    fixed_script = "/home/user/fixed_calc_variance.sh"
    log_file = "/home/user/mem_stats.log"

    assert os.path.exists(fixed_script), f"{fixed_script} does not exist."
    assert os.path.isfile(fixed_script), f"{fixed_script} is not a file."
    assert os.access(fixed_script, os.X_OK), f"{fixed_script} is not executable."

    # Calculate expected variances using Welford's algorithm in Python
    expected_vars = []
    n_count = 0
    mean = 0.0
    M2 = 0.0
    with open(log_file, "r") as f:
        for line in f:
            val = float(line.strip())
            n_count += 1
            delta = val - mean
            mean += delta / n_count
            M2 += delta * (val - mean)
            var = M2 / n_count
            expected_vars.append((n_count, var))

    # Run the fixed script
    try:
        out = subprocess.check_output([fixed_script, log_file], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Fixed script failed to run: {e}")

    lines = out.strip().splitlines()
    assert len(lines) == len(expected_vars), f"Expected {len(expected_vars)} lines of output, got {len(lines)}."

    for i, line in enumerate(lines):
        parts = line.split()
        assert len(parts) == 2, f"Line {i+1} of output is malformed: '{line}'"

        n_out = int(parts[0])
        var_out = float(parts[1])

        expected_n, expected_var = expected_vars[i]

        assert n_out == expected_n, f"Line {i+1}: expected n={expected_n}, got {n_out}."
        assert var_out >= 0, f"Line {i+1}: variance is negative ({var_out})."
        assert math.isclose(var_out, expected_var, rel_tol=1e-5, abs_tol=1e-5), \
            f"Line {i+1}: expected variance {expected_var}, got {var_out}."