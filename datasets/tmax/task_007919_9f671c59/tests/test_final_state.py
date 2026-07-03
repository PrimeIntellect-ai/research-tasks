# test_final_state.py

import os
import json
import pytest

RESULTS_PATH = "/home/user/results.json"

def test_results_file_exists():
    assert os.path.isfile(RESULTS_PATH), f"Expected results file {RESULTS_PATH} does not exist."

def test_results_format_and_values():
    with open(RESULTS_PATH, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON.")

    assert "query_vector" in results, "'query_vector' missing from results.json"
    assert "top_3_indices" in results, "'top_3_indices' missing from results.json"
    assert "benchmark_time_seconds" in results, "'benchmark_time_seconds' missing from results.json"

    # Validate query_vector
    expected_query_vector = [0.54, 0.24, 0.48, 0.18, 0.06]
    actual_query_vector = results["query_vector"]
    assert isinstance(actual_query_vector, list), "'query_vector' must be a list."
    assert len(actual_query_vector) == 5, "'query_vector' must have 5 elements."

    for expected, actual in zip(expected_query_vector, actual_query_vector):
        assert abs(expected - actual) < 1e-4, f"query_vector values incorrect. Expected {expected_query_vector}, got {actual_query_vector}."

    # Validate top_3_indices
    expected_indices = [0, 1, 5]
    actual_indices = results["top_3_indices"]
    assert actual_indices == expected_indices, f"top_3_indices incorrect. Expected {expected_indices}, got {actual_indices}."

    # Validate benchmark_time_seconds
    benchmark_time = results["benchmark_time_seconds"]
    assert isinstance(benchmark_time, (float, int)), "'benchmark_time_seconds' must be a number."
    assert benchmark_time > 0, "'benchmark_time_seconds' must be greater than 0."