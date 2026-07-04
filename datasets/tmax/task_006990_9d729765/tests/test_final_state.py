# test_final_state.py

import os
import json
import pytest
import math

def test_stats_json_exists():
    """Test that the stats.json file exists."""
    stats_path = '/home/user/stats.json'
    assert os.path.isfile(stats_path), f"Results file is missing: {stats_path}"

def test_stats_json_format_and_values():
    """Test that stats.json contains the correct keys and values."""
    stats_path = '/home/user/stats.json'
    assert os.path.isfile(stats_path), f"Results file is missing: {stats_path}"

    with open(stats_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("stats.json is not a valid JSON file.")

    assert "statistic" in data, "Key 'statistic' is missing from stats.json"
    assert "p_value" in data, "Key 'p_value' is missing from stats.json"

    # Expected values derived from the ground truth logic
    # stat should be approximately -69.176
    # pval should be approximately 3.9e-51
    expected_stat = -69.176
    expected_pval = 3.9e-51

    stat = data["statistic"]
    pval = data["p_value"]

    assert isinstance(stat, (int, float)), "statistic must be a number"
    assert isinstance(pval, (int, float)), "p_value must be a number"

    assert abs(stat - expected_stat) < 1.0, f"statistic {stat} is not close to expected {expected_stat}"
    assert pval < 1e-40, f"p_value {pval} is not close to expected {expected_pval}"