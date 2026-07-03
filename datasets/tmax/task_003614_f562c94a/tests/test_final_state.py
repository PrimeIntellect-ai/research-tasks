# test_final_state.py

import os
import json
import pytest

def test_stats_json_exists_and_valid():
    """Test that stats.json exists and contains the correct statistics."""
    json_path = "/home/user/stats.json"
    assert os.path.exists(json_path), f"The output file {json_path} is missing."
    assert os.path.isfile(json_path), f"The path {json_path} is not a file."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    # Check keys
    expected_keys = {"correlation_length_score", "covariance_ai_score", "filtered_count"}
    assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys}, but got {set(data.keys())}."

    # Check filtered_count
    assert data["filtered_count"] == 4, f"Expected filtered_count to be 4, but got {data['filtered_count']}."

    # Check correlation_length_score
    corr = data["correlation_length_score"]
    assert isinstance(corr, (int, float)), "correlation_length_score must be a number."
    assert abs(corr - 0.169136) < 0.001, f"Expected correlation_length_score around 0.169136, but got {corr}."

    # Check covariance_ai_score
    cov = data["covariance_ai_score"]
    assert isinstance(cov, (int, float)), "covariance_ai_score must be a number."
    assert abs(cov - 0.183333) < 0.001, f"Expected covariance_ai_score around 0.183333, but got {cov}."

def test_go_code_exists():
    """Test that the Go program exists at the specified location."""
    go_path = "/home/user/ml_prep/analyzer.go"
    assert os.path.exists(go_path), f"The Go source file {go_path} is missing."
    assert os.path.isfile(go_path), f"The path {go_path} is not a file."