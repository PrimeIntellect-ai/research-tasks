# test_final_state.py

import os
import json
import statistics
import pytest

def test_metrics_output_exists():
    """Verify that the metrics_output.json file was successfully generated."""
    file_path = "/home/user/metrics_output.json"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist. Did you run run_production.py successfully?"

def test_metrics_output_content():
    """Verify that the metrics_output.json contains the correct data and computed standard deviation."""
    file_path = "/home/user/metrics_output.json"

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {file_path} does not contain valid JSON.")

    # Assert basic structure and status
    assert data.get("status") == "success", "The 'status' field in the output JSON is not 'success'."
    assert data.get("retries_exhausted_gracefully") is True, "The 'retries_exhausted_gracefully' field should be True."

    # Compute the expected standard deviation to compare against the output
    dataset = [100000000.0, 100000000.1, 100000000.2]
    expected_stdev = round(statistics.stdev(dataset), 5)

    assert "standard_deviation" in data, "The 'standard_deviation' field is missing from the output JSON."

    actual_stdev = data["standard_deviation"]
    assert actual_stdev == expected_stdev, (
        f"The computed standard deviation is incorrect. "
        f"Expected {expected_stdev}, but got {actual_stdev}. "
        "Ensure you fixed the numerical instability bug in aggregator.py."
    )