# test_final_state.py
import os
import json
import math
import pytest

def test_results_file_exists():
    """Check if the results JSON file exists."""
    results_file = "/home/user/results.json"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

def test_results_content():
    """Check if the results JSON file contains the correct calculated values."""
    results_file = "/home/user/results.json"

    with open(results_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not a valid JSON.")

    expected_keys = {"matched_count", "total_gc", "total_bases", "average_gc_ratio"}
    missing_keys = expected_keys - results.keys()
    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"

    # Deterministic expected values based on the fixed random seed in setup
    expected_matched_count = 1494
    expected_total_bases = 222956
    expected_total_gc = 111306
    expected_average_gc_ratio = 0.499229

    assert isinstance(results["matched_count"], int), "matched_count must be an integer"
    assert results["matched_count"] == expected_matched_count, f"Expected matched_count to be {expected_matched_count}, got {results['matched_count']}"

    assert isinstance(results["total_bases"], int), "total_bases must be an integer"
    assert results["total_bases"] == expected_total_bases, f"Expected total_bases to be {expected_total_bases}, got {results['total_bases']}"

    assert isinstance(results["total_gc"], int), "total_gc must be an integer"
    assert results["total_gc"] == expected_total_gc, f"Expected total_gc to be {expected_total_gc}, got {results['total_gc']}"

    assert isinstance(results["average_gc_ratio"], float), "average_gc_ratio must be a float"
    assert math.isclose(results["average_gc_ratio"], expected_average_gc_ratio, rel_tol=1e-5), \
        f"Expected average_gc_ratio to be {expected_average_gc_ratio}, got {results['average_gc_ratio']}"