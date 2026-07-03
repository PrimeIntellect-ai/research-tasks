# test_final_state.py
import os
import json
import math
import pytest

def test_cpp_file_exists():
    assert os.path.isfile("/home/user/fit_dist.cpp"), "Expected C++ source file /home/user/fit_dist.cpp to exist."

def test_results_json_exists():
    assert os.path.isfile("/home/user/results.json"), "Expected /home/user/results.json to exist."

def test_results_json_contents():
    with open("/home/user/results.json", "r") as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/results.json is not valid JSON.")

    required_keys = {"lambda_opt", "ci_lower", "ci_upper", "stability_diff"}
    for key in required_keys:
        assert key in res, f"Key '{key}' missing from results.json"
        assert isinstance(res[key], (int, float)), f"Value for '{key}' must be a number."

    # Recompute best lambda based on data.txt
    assert os.path.isfile("/home/user/data.txt"), "data.txt is missing."
    with open("/home/user/data.txt", "r") as f:
        data = [float(line.strip()) for line in f if line.strip()]

    n = len(data)
    data_sorted = sorted(data)

    def cvm(lmbda):
        term_sum = 0.0
        for i, x in enumerate(data_sorted):
            cdf = 1.0 - math.exp(-lmbda * x)
            expected = (2 * (i + 1) - 1) / (2.0 * n)
            term_sum += (cdf - expected) ** 2
        return 1.0 / (12.0 * n) + term_sum

    # Grid search
    lambdas = [0.1 + i * 0.01 for i in range(491)] # 0.1 to 5.0 inclusive
    best_lambda = min(lambdas, key=cvm)

    # Check lambda_opt
    assert abs(res["lambda_opt"] - best_lambda) < 0.011, f"Expected lambda_opt ~ {best_lambda}, got {res['lambda_opt']}"

    # Check CI ranges
    assert 2.0 < res["ci_lower"] < best_lambda, f"ci_lower {res['ci_lower']} out of expected range (2.0, {best_lambda})"
    assert best_lambda < res["ci_upper"] < 3.0, f"ci_upper {res['ci_upper']} out of expected range ({best_lambda}, 3.0)"

    # Check stability diff
    assert res["stability_diff"] >= 0.0, "stability_diff should be non-negative."