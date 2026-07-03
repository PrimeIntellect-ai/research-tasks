# test_final_state.py

import os
import json
import pytest

def test_fit_plot_exists():
    plot_path = "/home/user/results/fit_plot.png"
    assert os.path.isfile(plot_path), f"Plot file {plot_path} does not exist."

    # Check if it's a valid PNG file by reading the magic number
    with open(plot_path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", f"File {plot_path} is not a valid PNG image."

def test_json_results_exist_and_valid():
    json_path = "/home/user/results/tm_posterior.json"
    assert os.path.isfile(json_path), f"JSON results file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    required_keys = ["tm_mean", "tm_2_5", "tm_97_5"]
    for key in required_keys:
        assert key in data, f"Key '{key}' is missing from {json_path}."
        assert isinstance(data[key], (int, float)), f"Value for '{key}' must be a number."

def test_posterior_values():
    json_path = "/home/user/results/tm_posterior.json"
    if not os.path.isfile(json_path):
        pytest.skip("JSON file missing.")

    with open(json_path, "r") as f:
        data = json.load(f)

    tm_mean = float(data.get("tm_mean", 0))
    tm_2_5 = float(data.get("tm_2_5", 0))
    tm_97_5 = float(data.get("tm_97_5", 0))

    assert 68.0 <= tm_mean <= 69.0, f"tm_mean ({tm_mean}) is out of expected bounds (68.0 - 69.0)."
    assert 67.0 <= tm_2_5 <= 68.5, f"tm_2_5 ({tm_2_5}) is out of expected bounds (67.0 - 68.5)."
    assert 68.5 <= tm_97_5 <= 70.0, f"tm_97_5 ({tm_97_5}) is out of expected bounds (68.5 - 70.0)."
    assert tm_2_5 < tm_mean < tm_97_5, f"Credible intervals are invalid: {tm_2_5} < {tm_mean} < {tm_97_5} is False."