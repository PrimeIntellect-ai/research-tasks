# test_final_state.py
import os
import re
import math
import pytest

BASE_DIR = "/home/user/calc_engine"
LOG_PATH = "/home/user/results.log"
DATA_PATH = os.path.join(BASE_DIR, "data.txt")
CONFIG_PATH = os.path.join(BASE_DIR, "config.h")
MAKEFILE_PATH = os.path.join(BASE_DIR, "Makefile")
SOLVER_PATH = os.path.join(BASE_DIR, "solver.c")

def test_makefile_fixed():
    assert os.path.isfile(MAKEFILE_PATH), f"Makefile missing at {MAKEFILE_PATH}"
    with open(MAKEFILE_PATH, "r") as f:
        content = f.read()
    assert "-lm" in content, "Makefile does not contain the '-lm' linker flag."

def test_config_fixed():
    assert os.path.isfile(CONFIG_PATH), f"config.h missing at {CONFIG_PATH}"
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    assert "15.42" in content, "config.h does not contain the recovered MAGIC_COEFF (15.420)."

def test_solver_c_convergence_fixed():
    assert os.path.isfile(SOLVER_PATH), f"solver.c missing at {SOLVER_PATH}"
    with open(SOLVER_PATH, "r") as f:
        content = f.read()
    # Check for absolute value usage in the termination condition
    # The user could use fabs(err), abs(err), or similar
    assert "abs(" in content or "err < -1e-6" in content, "solver.c does not seem to fix the convergence logic by taking the absolute value of err."

def test_results_log_exists():
    assert os.path.isfile(LOG_PATH), f"Results log missing at {LOG_PATH}"

def test_results_log_correctness():
    assert os.path.isfile(LOG_PATH), f"Results log missing at {LOG_PATH}"
    assert os.path.isfile(DATA_PATH), f"data.txt missing at {DATA_PATH}"

    # Extract valid floats from data.txt
    with open(DATA_PATH, "r") as f:
        tokens = f.read().split()

    valid_vals = []
    for token in tokens:
        try:
            valid_vals.append(float(token))
        except ValueError:
            pass

    # Recompute expected sum in Python
    def solve_py(val, coeff=15.420):
        x = 1.0
        def f(x): return x * math.exp(x) - (val + coeff)
        def df(x): return math.exp(x) * (1.0 + x)

        err = f(x)
        iter_count = 0
        while abs(err) > 1e-6 and iter_count < 1000:
            x = x - err / df(x)
            err = f(x)
            iter_count += 1
        return x

    expected_sum = sum(solve_py(v) for v in valid_vals)

    # Read the actual result
    with open(LOG_PATH, "r") as f:
        log_content = f.read()

    match = re.search(r"Total Sum:\s*([0-9.]+)", log_content)
    assert match is not None, f"Could not find 'Total Sum: <value>' in {LOG_PATH}. File content: {log_content}"

    actual_sum = float(match.group(1))

    assert math.isclose(actual_sum, expected_sum, rel_tol=1e-3), \
        f"Expected total sum to be approximately {expected_sum:.5f}, but got {actual_sum}. " \
        "Check input parsing and convergence logic."