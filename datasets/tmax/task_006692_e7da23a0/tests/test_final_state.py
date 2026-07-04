# test_final_state.py

import os
import json
import math
import pytest

def test_analysis_results_exists():
    """Check if the analysis_results.json file was created."""
    file_path = "/home/user/analysis_results.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The script must create this file."

def test_analysis_results_structure_and_types():
    """Validate the structure, keys, and types of the output JSON."""
    file_path = "/home/user/analysis_results.json"
    if not os.path.isfile(file_path):
        pytest.skip("JSON file missing.")

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file analysis_results.json is not valid JSON.")

    expected_keys = {"t1_temperatures", "wasserstein_distances", "wilcoxon_p_value"}
    actual_keys = set(data.keys())
    assert expected_keys.issubset(actual_keys), f"Missing keys in JSON. Expected {expected_keys}, found {actual_keys}."

    t1 = data["t1_temperatures"]
    wd = data["wasserstein_distances"]
    pval = data["wilcoxon_p_value"]

    assert isinstance(t1, list), "'t1_temperatures' must be a list."
    assert isinstance(wd, list), "'wasserstein_distances' must be a list."
    assert isinstance(pval, float) or isinstance(pval, int), "'wilcoxon_p_value' must be a float."

    assert len(t1) == 10, f"Expected 10 values for 't1_temperatures', got {len(t1)}."
    assert len(wd) == 10, f"Expected 10 values for 'wasserstein_distances', got {len(wd)}."

    assert all(isinstance(x, (float, int)) for x in t1), "All items in 't1_temperatures' must be numbers."
    assert all(isinstance(x, (float, int)) for x in wd), "All items in 'wasserstein_distances' must be numbers."

def test_analysis_results_values():
    """Validate the values inside the output JSON for correctness."""
    file_path = "/home/user/analysis_results.json"
    if not os.path.isfile(file_path):
        pytest.skip("JSON file missing.")

    with open(file_path, "r") as f:
        data = json.load(f)

    t1 = data.get("t1_temperatures", [])
    wd = data.get("wasserstein_distances", [])
    pval = data.get("wilcoxon_p_value", -1.0)

    if len(t1) == 10:
        assert math.isclose(t1[0], 1000.0, abs_tol=1.0), f"Initial T1 temperature should be 1000.0, got {t1[0]}"
        assert math.isclose(t1[-1], 292.8, abs_tol=5.0), f"Final T1 temperature at t=90 should be approx 292.8, got {t1[-1]}"

    if len(wd) == 10:
        assert all(w >= 0.0 for w in wd), "Wasserstein distances cannot be negative."

    assert 0.0 <= pval <= 1.0, f"Wilcoxon p-value must be between 0.0 and 1.0, got {pval}"