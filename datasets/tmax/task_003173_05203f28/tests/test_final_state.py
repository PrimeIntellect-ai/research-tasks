# test_final_state.py

import os
import struct
import math
import pytest

def test_profiler_stats_files_exist():
    assert os.path.exists("/home/user/profiler_stats.c"), "/home/user/profiler_stats.c does not exist."
    assert os.path.exists("/home/user/profiler_stats"), "/home/user/profiler_stats executable does not exist."
    assert os.access("/home/user/profiler_stats", os.X_OK), "/home/user/profiler_stats is not executable."

def test_stats_output_correctness():
    output_file = "/home/user/stats_output.txt"
    assert os.path.exists(output_file), f"{output_file} does not exist."

    # Read binary data to compute truth
    bin_file = "/home/user/execution_times.bin"
    assert os.path.exists(bin_file), f"{bin_file} is missing."

    with open(bin_file, "rb") as f:
        data_bytes = f.read()

    num_doubles = len(data_bytes) // 8
    assert num_doubles == 1000000, "Expected 1,000,000 doubles in the binary file."

    # Unpack doubles
    data = struct.unpack(f"{num_doubles}d", data_bytes)

    # Calculate truth values
    n = len(data)
    mean = sum(data) / n
    est_lambda = 1.0 / mean

    # Empirical variance (ddof=1)
    # Using math.fsum for better precision if needed, but standard sum is fine for this check.
    # We'll use a 2-pass algorithm for variance to match standard unbiased estimator
    sq_diffs = sum((x - mean) ** 2 for x in data)
    emp_var = sq_diffs / (n - 1)

    analyt_var = 1.0 / (est_lambda ** 2)

    # Parse output file
    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {output_file}, found {len(lines)}."

    parsed_lambda = None
    parsed_emp_var = None
    parsed_analyt_var = None

    for line in lines:
        if line.startswith("Estimated Lambda:"):
            parsed_lambda = float(line.split(":")[1].strip())
        elif line.startswith("Empirical Variance:"):
            parsed_emp_var = float(line.split(":")[1].strip())
        elif line.startswith("Analytical Variance:"):
            parsed_analyt_var = float(line.split(":")[1].strip())

    assert parsed_lambda is not None, "Could not find 'Estimated Lambda:' in output."
    assert parsed_emp_var is not None, "Could not find 'Empirical Variance:' in output."
    assert parsed_analyt_var is not None, "Could not find 'Analytical Variance:' in output."

    # Check with tolerance
    tol = 0.00005
    assert abs(parsed_lambda - est_lambda) <= tol, f"Estimated Lambda {parsed_lambda} is not within {tol} of expected {est_lambda:.5f}."
    assert abs(parsed_emp_var - emp_var) <= tol, f"Empirical Variance {parsed_emp_var} is not within {tol} of expected {emp_var:.5f}."
    assert abs(parsed_analyt_var - analyt_var) <= tol, f"Analytical Variance {parsed_analyt_var} is not within {tol} of expected {analyt_var:.5f}."