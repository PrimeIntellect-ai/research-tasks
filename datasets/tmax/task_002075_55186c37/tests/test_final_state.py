# test_final_state.py

import os
import json
import pytest
import math

def test_summary_json_exists():
    """Test that the summary.json file exists."""
    assert os.path.exists("/home/user/summary.json"), "The file /home/user/summary.json does not exist."
    assert os.path.isfile("/home/user/summary.json"), "/home/user/summary.json is not a file."

def test_summary_json_content():
    """Test that the summary.json contains the correct computed values based on the data schema and LCG."""
    with open("/home/user/summary.json", "r", encoding="utf-8") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/summary.json does not contain valid JSON.")

    # Recompute the expected results
    m = 2**31
    a = 1103515245
    c = 12345
    seed = 42

    def next_rand():
        nonlocal seed
        seed = (a * seed + c) % m
        return seed

    # The data derived from dropping invalid rows in experiments.csv
    data = {
        "exp_A": [10.0, 11.0, 14.0],
        "exp_B": [15.5, 16.2, 17.0]
    }

    expected_results = {}
    for exp_id in sorted(data.keys()):
        T = data[exp_id]
        L = len(T)
        boot_means = []
        for _ in range(1000):
            sample_sum = 0
            for _ in range(L):
                idx = next_rand() % L
                sample_sum += T[idx]
            boot_means.append(sample_sum / L)

        boot_means.sort()
        expected_results[exp_id] = {
            "mean": round(sum(T)/L, 2),
            "ci_lower": round(boot_means[25], 2),
            "ci_upper": round(boot_means[975], 2),
            "valid_samples": L
        }

    # Verify keys
    assert set(results.keys()) == set(expected_results.keys()), \
        f"Expected experiment IDs {list(expected_results.keys())}, but got {list(results.keys())}"

    # Verify values
    for exp_id, expected_stats in expected_results.items():
        actual_stats = results[exp_id]
        for stat, expected_val in expected_stats.items():
            assert stat in actual_stats, f"Missing '{stat}' in results for {exp_id}"
            actual_val = actual_stats[stat]
            assert math.isclose(actual_val, expected_val, rel_tol=1e-5, abs_tol=1e-2), \
                f"For {exp_id} '{stat}', expected {expected_val} but got {actual_val}"