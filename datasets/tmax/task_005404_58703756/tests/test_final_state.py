# test_final_state.py

import os
import json
import math
import pytest

REPORT_PATH = "/home/user/metrics_report.json"

def test_metrics_report_exists():
    """Test that the metrics report JSON file was created."""
    assert os.path.exists(REPORT_PATH), f"File {REPORT_PATH} was not created."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file."

def test_metrics_report_content():
    """Test that the metrics report contains the correctly computed values."""
    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    expected_keys = {
        "cleaned_row_count",
        "mean_memory_ratio",
        "cpu_usage_bootstrap_mean",
        "cpu_usage_95_ci_lower",
        "cpu_usage_95_ci_upper"
    }

    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected keys. Found: {list(data.keys())}"

    # Check cleaned_row_count
    assert data["cleaned_row_count"] == 6, f"Expected cleaned_row_count to be 6, got {data['cleaned_row_count']}"

    # Check mean_memory_ratio
    expected_memory_ratio = 0.5052
    assert math.isclose(data["mean_memory_ratio"], expected_memory_ratio, abs_tol=1e-3), \
        f"Expected mean_memory_ratio close to {expected_memory_ratio}, got {data['mean_memory_ratio']}"

    # Check bootstrap statistics
    expected_boot_mean = 50.2982
    expected_ci_lower = 45.5333
    expected_ci_upper = 55.1500

    assert math.isclose(data["cpu_usage_bootstrap_mean"], expected_boot_mean, abs_tol=1e-2), \
        f"Expected cpu_usage_bootstrap_mean close to {expected_boot_mean}, got {data['cpu_usage_bootstrap_mean']}"

    assert math.isclose(data["cpu_usage_95_ci_lower"], expected_ci_lower, abs_tol=1e-2), \
        f"Expected cpu_usage_95_ci_lower close to {expected_ci_lower}, got {data['cpu_usage_95_ci_lower']}"

    assert math.isclose(data["cpu_usage_95_ci_upper"], expected_ci_upper, abs_tol=1e-2), \
        f"Expected cpu_usage_95_ci_upper close to {expected_ci_upper}, got {data['cpu_usage_95_ci_upper']}"