# test_final_state.py
import os
import json
import math

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"File {results_path} does not exist. The pipeline may not have run successfully."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_path} is not valid JSON."

    expected_keys = [
        "imputed_feature_x_median",
        "t_statistic",
        "regression_slope",
        "regression_intercept"
    ]

    for key in expected_keys:
        assert key in results, f"Key '{key}' is missing from {results_path}."

    # Check median
    assert results["imputed_feature_x_median"] == 60, \
        f"Expected imputed_feature_x_median to be 60, got {results['imputed_feature_x_median']}"

    # Check t_statistic
    t_stat = results["t_statistic"]
    assert isinstance(t_stat, (int, float)), "t_statistic must be a number"
    assert math.isclose(t_stat, 1.7645, abs_tol=0.005), \
        f"Expected t_statistic to be approx 1.7645, got {t_stat}"

    # Check regression_slope
    slope = results["regression_slope"]
    assert isinstance(slope, (int, float)), "regression_slope must be a number"
    assert math.isclose(slope, 2.3787, abs_tol=0.005), \
        f"Expected regression_slope to be approx 2.3787, got {slope}"

    # Check regression_intercept
    intercept = results["regression_intercept"]
    assert isinstance(intercept, (int, float)), "regression_intercept must be a number"
    assert math.isclose(intercept, 17.4363, abs_tol=0.005), \
        f"Expected regression_intercept to be approx 17.4363, got {intercept}"