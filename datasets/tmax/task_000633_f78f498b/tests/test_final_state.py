# test_final_state.py
import os
import pytest
import numpy as np
from scipy.stats import wasserstein_distance

def test_all_runs_txt():
    path = "/home/user/all_runs.txt"
    assert os.path.exists(path), f"The file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1000, f"Expected exactly 1000 lines in {path}, but found {len(lines)}."

    success_count = sum(1 for line in lines if line.startswith("SUCCESS"))
    fail_count = sum(1 for line in lines if line.startswith("FAIL"))
    assert success_count + fail_count == 1000, "All lines must start with either 'SUCCESS' or 'FAIL'."

def test_distance_script_exists():
    path = "/home/user/distance.py"
    assert os.path.exists(path), f"The python script {path} does not exist."

def test_result_txt():
    path = "/home/user/result.txt"
    assert os.path.exists(path), f"The file {path} does not exist."

    # Compute expected result
    success_conds = []
    fail_conds = []

    for seed in range(1, 1001):
        np.random.seed(seed)
        A = np.random.randn(50, 50)
        if seed % 7 == 0:
            A[1] = A[0] + np.random.randn(50) * 1e-14

        cond = np.linalg.cond(A)
        if cond > 1e11:
            fail_conds.append(cond)
        else:
            success_conds.append(cond)

    expected_distance = round(wasserstein_distance(success_conds, fail_conds), 2)

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        actual_distance = float(content)
    except ValueError:
        pytest.fail(f"Could not parse a float from {path}. Content found: '{content}'")

    assert actual_distance == expected_distance, f"Expected Wasserstein distance {expected_distance}, but got {actual_distance}."