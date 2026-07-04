# test_final_state.py
import os
import json
import math
import pytest

def test_stats_json_exists_and_valid():
    stats_path = '/home/user/stats.json'
    assert os.path.isfile(stats_path), f"Expected JSON file missing: {stats_path}"

    with open(stats_path, 'r') as f:
        try:
            stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {stats_path} is not valid JSON.")

    expected_keys = {"500", "1000", "1500"}
    assert set(stats.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, got {set(stats.keys())}"

    for key in expected_keys:
        val = stats[key]
        assert isinstance(val, float) or isinstance(val, int), f"Value for key '{key}' must be a number, got {type(val)}"

def test_statistical_results():
    stats_path = '/home/user/stats.json'
    if not os.path.isfile(stats_path):
        pytest.skip("stats.json not found")

    with open(stats_path, 'r') as f:
        stats = json.load(f)

    # The treatment group has a significantly higher peak at 1000, 
    # while peaks at 500 and 1500 remain the same as the control group.
    # Therefore, p-value for 1000 should be extremely small, and others should be > 0.05.

    p_500 = float(stats.get("500", 0))
    p_1000 = float(stats.get("1000", 1))
    p_1500 = float(stats.get("1500", 0))

    assert p_1000 < 1e-3, f"Expected highly significant p-value (< 1e-3) for peak 1000, got {p_1000}"
    assert p_500 > 0.01, f"Expected non-significant p-value (> 0.01) for peak 500, got {p_500}"
    assert p_1500 > 0.01, f"Expected non-significant p-value (> 0.01) for peak 1500, got {p_1500}"

def test_mean_spectra_plot_exists():
    plot_path = '/home/user/mean_spectra.png'
    assert os.path.isfile(plot_path), f"Expected plot file missing: {plot_path}"
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty."