# test_final_state.py

import os
import json
import pytest
import math

def test_results_file_exists():
    assert os.path.isfile('/home/user/results.json'), "The results file /home/user/results.json does not exist."

def test_results_structure():
    with open('/home/user/results.json', 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    assert "mse" in results, "Key 'mse' missing from results.json."
    assert "corrupted_batches" in results, "Key 'corrupted_batches' missing from results.json."

    expected_mse_keys = {"clean", "batch_1", "batch_2", "batch_3"}
    assert set(results["mse"].keys()) == expected_mse_keys, f"Expected mse keys {expected_mse_keys}, got {set(results['mse'].keys())}."

    for k, v in results["mse"].items():
        assert isinstance(v, float), f"MSE value for {k} is not a float."

    assert set(results["corrupted_batches"].keys()) == {"batch_2"}, "Only 'batch_2' should be identified as corrupted."

    b2_stats = results["corrupted_batches"]["batch_2"]
    expected_stat_keys = {"t_statistic", "p_value", "ci_lower", "ci_upper"}
    assert set(b2_stats.keys()) == expected_stat_keys, f"Expected stats keys {expected_stat_keys}, got {set(b2_stats.keys())}."

    for k, v in b2_stats.items():
        assert isinstance(v, float), f"Value for {k} in corrupted_batches is not a float."

def test_results_values():
    with open('/home/user/results.json', 'r') as f:
        results = json.load(f)

    mse_b2 = results["mse"]["batch_2"]
    assert mse_b2 > 2.0, f"MSE for batch_2 should be > 2.0, got {mse_b2}"

    mse_clean = results["mse"]["clean"]
    mse_b1 = results["mse"]["batch_1"]
    mse_b3 = results["mse"]["batch_3"]

    assert mse_clean < 2.0, f"MSE for clean should be < 2.0, got {mse_clean}"
    assert mse_b1 < 2.0, f"MSE for batch_1 should be < 2.0, got {mse_b1}"
    assert mse_b3 < 2.0, f"MSE for batch_3 should be < 2.0, got {mse_b3}"

    t_stat = results["corrupted_batches"]["batch_2"]["t_statistic"]
    assert t_stat > 0, f"t_statistic for batch_2 should be positive, got {t_stat}"

    ci_lower = results["corrupted_batches"]["batch_2"]["ci_lower"]
    ci_upper = results["corrupted_batches"]["batch_2"]["ci_upper"]
    assert ci_lower < ci_upper, "ci_lower should be less than ci_upper."