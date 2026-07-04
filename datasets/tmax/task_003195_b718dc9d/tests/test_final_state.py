# test_final_state.py

import os
import json
import math
import pytest

RESULTS_FILE = "/home/user/results.json"

def test_results_file_exists():
    """Check if the results.json file was created."""
    assert os.path.isfile(RESULTS_FILE), f"The file {RESULTS_FILE} does not exist. Did you run your script?"

def test_results_content_and_accuracy():
    """Parse results.json and verify the calculated metrics."""
    assert os.path.isfile(RESULTS_FILE), f"Missing {RESULTS_FILE}"

    with open(RESULTS_FILE, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULTS_FILE} does not contain valid JSON.")

    assert "parallel_fraction" in results, f"Key 'parallel_fraction' is missing from {RESULTS_FILE}"
    assert "wasserstein_distance" in results, f"Key 'wasserstein_distance' is missing from {RESULTS_FILE}"

    p_frac = results["parallel_fraction"]
    w_dist = results["wasserstein_distance"]

    assert isinstance(p_frac, (int, float)), "parallel_fraction must be a number"
    assert isinstance(w_dist, (int, float)), "wasserstein_distance must be a number"

    expected_p_frac = 0.8
    expected_w_dist = 70.0

    assert math.isclose(p_frac, expected_p_frac, abs_tol=0.05), \
        f"parallel_fraction {p_frac} is not within the expected range (expected ~{expected_p_frac})"

    assert math.isclose(w_dist, expected_w_dist, abs_tol=2.0), \
        f"wasserstein_distance {w_dist} is not within the expected range (expected ~{expected_w_dist})"