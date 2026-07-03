# test_final_state.py
import os
import re

def test_mc_regression_script():
    script_path = "/home/user/mc_regression.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_run_convergence_script():
    script_path = "/home/user/run_convergence.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_convergence_log_contents():
    log_path = "/home/user/convergence_log.csv"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    expected_values = [
        (10, 3.73801, 1.83921),
        (100, 3.42436, 2.04683),
        (1000, 3.52288, 1.99616),
        (10000, 3.49818, 2.00067),
        (100000, 3.49987, 2.00002)
    ]

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_values), f"Expected {len(expected_values)} lines in {log_path}, found {len(lines)}."

    for i, (line, expected) in enumerate(zip(lines, expected_values)):
        # Split by comma and strip whitespace
        parts = [p.strip() for p in line.split(",")]
        assert len(parts) == 3, f"Line {i+1} does not have exactly 3 comma-separated values: '{line}'"

        try:
            n = int(parts[0])
            m = float(parts[1])
            c = float(parts[2])
        except ValueError:
            assert False, f"Line {i+1} contains non-numeric values: '{line}'"

        exp_n, exp_m, exp_c = expected

        assert n == exp_n, f"Line {i+1}: Expected N={exp_n}, got N={n}"
        assert abs(m - exp_m) < 1e-5, f"Line {i+1}: Expected m={exp_m}, got m={m}"
        assert abs(c - exp_c) < 1e-5, f"Line {i+1}: Expected c={exp_c}, got c={c}"