# test_final_state.py
import json
import os
import pytest

def test_alignment_stats_json():
    json_path = "/home/user/alignment_stats.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."
    assert os.path.isfile(json_path), f"Path {json_path} is not a file."

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON format in alignment_stats.json.")

    required_keys = ["observed_mms", "background_mean", "background_std", "z_score"]
    for key in required_keys:
        assert key in results, f"Missing key in JSON output: {key}"

    # Expected values
    EXPECTED_OBSERVED = 5
    EXPECTED_MEAN = 3.425
    EXPECTED_STD = 0.610

    assert results["observed_mms"] == EXPECTED_OBSERVED, \
        f"Incorrect observed_mms. Expected {EXPECTED_OBSERVED}, got {results['observed_mms']}"

    assert abs(results["background_mean"] - EXPECTED_MEAN) <= 0.05, \
        f"Background mean out of bounds. Got {results['background_mean']}, expected ~{EXPECTED_MEAN}"

    assert abs(results["background_std"] - EXPECTED_STD) <= 0.05, \
        f"Background std out of bounds. Got {results['background_std']}, expected ~{EXPECTED_STD}"

    expected_z = (results["observed_mms"] - results["background_mean"]) / results["background_std"]
    assert abs(results["z_score"] - expected_z) <= 0.05, \
        f"Z-score mathematically incorrect based on provided mean/std. Got {results['z_score']}, expected ~{expected_z}"