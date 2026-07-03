# test_final_state.py
import os
import json

def test_analysis_result_exists():
    file_path = '/home/user/analysis_result.json'
    assert os.path.isfile(file_path), f"Expected output file {file_path} is missing."

def test_analysis_result_format_and_values():
    file_path = '/home/user/analysis_result.json'
    assert os.path.isfile(file_path), f"Expected output file {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    expected_keys = {"mean_k_UI", "mean_k_IB", "p_k_UI_greater_k_IB", "reject_null"}
    actual_keys = set(data.keys())
    assert expected_keys.issubset(actual_keys), f"Missing keys in JSON. Expected {expected_keys}, found {actual_keys}."

    mean_k_UI = data["mean_k_UI"]
    mean_k_IB = data["mean_k_IB"]
    p_k_UI_greater_k_IB = data["p_k_UI_greater_k_IB"]
    reject_null = data["reject_null"]

    assert isinstance(mean_k_UI, (int, float)), f"mean_k_UI must be a float, got {type(mean_k_UI)}"
    assert isinstance(mean_k_IB, (int, float)), f"mean_k_IB must be a float, got {type(mean_k_IB)}"
    assert isinstance(p_k_UI_greater_k_IB, (int, float)), f"p_k_UI_greater_k_IB must be a float, got {type(p_k_UI_greater_k_IB)}"
    assert isinstance(reject_null, bool), f"reject_null must be a boolean, got {type(reject_null)}"

    assert 1.0 < mean_k_UI < 1.4, f"mean_k_UI out of expected bounds (1.0, 1.4): {mean_k_UI}"
    assert 0.2 < mean_k_IB < 0.6, f"mean_k_IB out of expected bounds (0.2, 0.6): {mean_k_IB}"
    assert p_k_UI_greater_k_IB > 0.95, f"p_k_UI_greater_k_IB should be > 0.95, got {p_k_UI_greater_k_IB}"
    assert reject_null is True, f"reject_null should be True, got {reject_null}"