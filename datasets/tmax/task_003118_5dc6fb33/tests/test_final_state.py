# test_final_state.py
import os
import json

def test_results_json_exists_and_valid():
    file_path = "/home/user/results.json"

    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise AssertionError(f"The file {file_path} does not contain valid JSON.")

    expected_keys = ["k1", "k2", "auc_plasma", "kl_divergence"]
    for key in expected_keys:
        assert key in data, f"Missing key '{key}' in {file_path}."
        assert isinstance(data[key], (int, float)), f"Value for '{key}' must be a number."

    k1 = data["k1"]
    k2 = data["k2"]
    auc_plasma = data["auc_plasma"]
    kl_divergence = data["kl_divergence"]

    assert 0.48 <= k1 <= 0.52, f"k1 value {k1} is out of expected bounds [0.48, 0.52]."
    assert 0.18 <= k2 <= 0.22, f"k2 value {k2} is out of expected bounds [0.18, 0.22]."
    assert 15.1 <= auc_plasma <= 15.5, f"auc_plasma value {auc_plasma} is out of expected bounds [15.1, 15.5]."
    assert 0.0001 <= kl_divergence <= 0.002, f"kl_divergence value {kl_divergence} is out of expected bounds [0.0001, 0.002]."