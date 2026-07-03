# test_final_state.py
import os
import json
import pytest

def test_model_results_exists():
    file_path = "/home/user/model_results.json"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_model_results_content_and_invariants():
    file_path = "/home/user/model_results.json"

    with open(file_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not a valid JSON file.")

    expected_keys = {
        "best_model",
        "aic_exponential",
        "aic_hyperbolic",
        "param1_estimate",
        "param1_ci_lower",
        "param1_ci_upper"
    }

    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"Missing keys in JSON: {missing_keys}"

    extra_keys = set(results.keys()) - expected_keys
    assert not extra_keys, f"Unexpected extra keys in JSON: {extra_keys}"

    # Check types
    assert isinstance(results["best_model"], str), "best_model must be a string."
    for key in ["aic_exponential", "aic_hyperbolic", "param1_estimate", "param1_ci_lower", "param1_ci_upper"]:
        assert isinstance(results[key], (int, float)), f"{key} must be a number."

    # The true underlying process is Exponential, so it should have a lower AIC and be chosen as best.
    assert results["best_model"] == "Exponential", "The Exponential model should be identified as the best_model."
    assert results["aic_exponential"] < results["aic_hyperbolic"], "AIC for Exponential should be lower than Hyperbolic."

    # The true parameter L is 12.0. The estimate should be reasonably close to it.
    est = results["param1_estimate"]
    assert 10.0 < est < 14.0, f"param1_estimate ({est}) is far from the expected true value (~12.0)."

    # Check confidence interval invariants
    ci_lower = results["param1_ci_lower"]
    ci_upper = results["param1_ci_upper"]

    assert ci_lower <= est, "Confidence interval lower bound must be <= the estimate."
    assert est <= ci_upper, "Confidence interval upper bound must be >= the estimate."
    assert ci_lower < ci_upper, "Confidence interval lower bound must be strictly less than the upper bound."
    assert ci_lower > 0, "Confidence interval lower bound should be positive for this physical process."