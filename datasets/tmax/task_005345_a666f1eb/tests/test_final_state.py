# test_final_state.py

import os
import json
import pytest

def test_cleaned_embeddings_exists():
    path = "/home/user/cleaned_embeddings.npy"
    assert os.path.isfile(path), f"Required file is missing: {path}"
    assert os.path.getsize(path) > 0, f"File {path} is empty"

def test_report_json_structure_and_values():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"Required file is missing: {path}"

    with open(path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not a valid JSON file")

    expected_keys = {
        "cleaned_count",
        "mean_latency_alpha",
        "mean_latency_beta",
        "t_statistic",
        "p_value",
        "ci_95_lower",
        "ci_95_upper"
    }

    missing_keys = expected_keys - set(report.keys())
    extra_keys = set(report.keys()) - expected_keys
    assert not missing_keys, f"report.json is missing keys: {missing_keys}"
    assert not extra_keys, f"report.json has unexpected extra keys: {extra_keys}"

    # Validate types
    assert isinstance(report["cleaned_count"], int), "cleaned_count must be an integer"
    assert report["cleaned_count"] > 0, "cleaned_count must be greater than 0"

    for key in ["mean_latency_alpha", "mean_latency_beta", "t_statistic", "p_value", "ci_95_lower", "ci_95_upper"]:
        assert isinstance(report[key], (int, float)), f"{key} must be a float"

    # Validate realistic latency values based on the mock inference API
    mean_alpha = report["mean_latency_alpha"]
    mean_beta = report["mean_latency_beta"]

    assert 0.001 < mean_alpha < 0.1, f"mean_latency_alpha ({mean_alpha}) is outside realistic bounds"
    assert 0.001 < mean_beta < 0.1, f"mean_latency_beta ({mean_beta}) is outside realistic bounds"

    # Validate statistical logic
    t_stat = report["t_statistic"]
    if mean_alpha > mean_beta:
        assert t_stat > 0, "t_statistic should be positive if mean_alpha > mean_beta"
    elif mean_alpha < mean_beta:
        assert t_stat < 0, "t_statistic should be negative if mean_alpha < mean_beta"

    p_val = report["p_value"]
    assert 0.0 <= p_val <= 1.0, f"p_value ({p_val}) must be between 0 and 1"

    ci_lower = report["ci_95_lower"]
    ci_upper = report["ci_95_upper"]
    assert ci_lower <= ci_upper, f"ci_95_lower ({ci_lower}) must be less than or equal to ci_95_upper ({ci_upper})"