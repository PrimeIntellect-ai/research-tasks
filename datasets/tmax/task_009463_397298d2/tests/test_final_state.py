# test_final_state.py

import os
import json
import pytest

def test_artifacts_directory_exists():
    """Test that the artifacts directory was created."""
    assert os.path.isdir("/home/user/artifacts"), "The artifacts directory /home/user/artifacts does not exist."

def test_run_metrics_json_exists():
    """Test that the run_metrics.json file was generated."""
    assert os.path.isfile("/home/user/artifacts/run_metrics.json"), "The file /home/user/artifacts/run_metrics.json was not found."

def test_run_metrics_schema_and_values():
    """Test that the run_metrics.json contains the correct schema and expected values."""
    metrics_path = "/home/user/artifacts/run_metrics.json"

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file run_metrics.json does not contain valid JSON.")

    expected_keys = {
        "vocab_size",
        "original_top_sv",
        "bootstrap_mean_sv",
        "ci_lower",
        "ci_upper"
    }

    assert set(metrics.keys()) == expected_keys, f"JSON keys do not match expected schema. Found: {list(metrics.keys())}"

    # Check types
    assert isinstance(metrics["vocab_size"], int), "vocab_size must be an integer."
    assert isinstance(metrics["original_top_sv"], float), "original_top_sv must be a float."
    assert isinstance(metrics["bootstrap_mean_sv"], float), "bootstrap_mean_sv must be a float."
    assert isinstance(metrics["ci_lower"], float), "ci_lower must be a float."
    assert isinstance(metrics["ci_upper"], float), "ci_upper must be a float."

    # Check values with a small tolerance for floating point and SVD solver differences
    assert metrics["vocab_size"] == 22, f"Expected vocab_size 22, got {metrics['vocab_size']}"

    # Check original_top_sv
    assert abs(metrics["original_top_sv"] - 4.1485) <= 0.001, \
        f"Expected original_top_sv around 4.1485, got {metrics['original_top_sv']}"

    # Check bootstrap_mean_sv
    assert abs(metrics["bootstrap_mean_sv"] - 4.3989) <= 0.001, \
        f"Expected bootstrap_mean_sv around 4.3989, got {metrics['bootstrap_mean_sv']}"

    # Check ci_lower
    assert abs(metrics["ci_lower"] - 3.0315) <= 0.001, \
        f"Expected ci_lower around 3.0315, got {metrics['ci_lower']}"

    # Check ci_upper
    assert abs(metrics["ci_upper"] - 5.8606) <= 0.001, \
        f"Expected ci_upper around 5.8606, got {metrics['ci_upper']}"

    # Check if values are properly rounded to 4 decimal places
    for key in ["original_top_sv", "bootstrap_mean_sv", "ci_lower", "ci_upper"]:
        val_str = str(metrics[key])
        if "." in val_str:
            decimals = len(val_str.split(".")[1])
            assert decimals <= 4, f"Value for {key} ({metrics[key]}) is not rounded to 4 decimal places."