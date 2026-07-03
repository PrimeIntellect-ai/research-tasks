# test_final_state.py

import os
import json
import math
import pytest

def test_parquet_partitioning():
    """Verify that the processed data directory exists and contains correct Parquet partitions."""
    processed_dir = "/home/user/processed_data"
    assert os.path.exists(processed_dir), f"Directory {processed_dir} does not exist."
    assert os.path.isdir(processed_dir), f"Path {processed_dir} is not a directory."

    locations = [f"LOC_{i:03d}" for i in range(1, 6)]
    for loc in locations:
        partition_dir = os.path.join(processed_dir, f"location_id={loc}")
        assert os.path.exists(partition_dir), f"Partition directory {partition_dir} does not exist. Parquet data must be partitioned by location_id."
        assert os.path.isdir(partition_dir), f"Path {partition_dir} is not a directory."

        # Verify that the partition directory contains files (the actual Parquet data)
        files = os.listdir(partition_dir)
        assert len(files) > 0, f"Partition directory {partition_dir} is empty. It should contain Parquet files."

def test_correlation_results():
    """Verify that the correlation results JSON is correctly structured and contains the right values."""
    results_file = "/home/user/results/top_correlation.json"
    assert os.path.exists(results_file), f"Results file {results_file} does not exist."
    assert os.path.isfile(results_file), f"Path {results_file} is not a file."

    with open(results_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} does not contain valid JSON.")

    # Check for required keys
    for key in ["var1", "var2", "correlation"]:
        assert key in data, f"Key '{key}' is missing in the JSON file."

    # Check variable names (alphabetically sorted)
    assert data["var1"] == "no2", f"Expected var1 to be 'no2', got '{data['var1']}'."
    assert data["var2"] == "traffic_volume", f"Expected var2 to be 'traffic_volume', got '{data['var2']}'."

    # Check correlation value
    correlation = data["correlation"]
    assert isinstance(correlation, (int, float)), f"Expected correlation to be a number, got {type(correlation).__name__}."

    # The expected correlation is ~0.9232 based on the seed
    expected_correlation = 0.9232
    assert math.isclose(correlation, expected_correlation, abs_tol=0.0002), \
        f"Expected correlation to be approximately {expected_correlation}, got {correlation}."