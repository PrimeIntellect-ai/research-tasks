# test_final_state.py
import os
import json
import math
import pytest

def test_fit_model_script_exists():
    script_path = '/home/user/fit_model.py'
    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_model_results_json_exists_and_format():
    json_path = '/home/user/model_results.json'
    assert os.path.exists(json_path), f"The results file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} is not valid JSON.")

    assert "frequencies" in data, "The key 'frequencies' is missing from the JSON output."
    assert "weights_chunk_0" in data, "The key 'weights_chunk_0' is missing from the JSON output."

    assert isinstance(data["frequencies"], list), "'frequencies' should be a list."
    assert isinstance(data["weights_chunk_0"], list), "'weights_chunk_0' should be a list."

def test_model_results_values():
    json_path = '/home/user/model_results.json'
    with open(json_path, 'r') as f:
        data = json.load(f)

    freqs = data.get("frequencies", [])
    assert len(freqs) == 2, f"Expected exactly 2 dominant frequencies, got {len(freqs)}."

    # Frequencies should be sorted in ascending order and match 5.0 and 12.0
    assert math.isclose(freqs[0], 5.0, abs_tol=0.05), f"Expected first frequency to be ~5.0, got {freqs[0]}."
    assert math.isclose(freqs[1], 12.0, abs_tol=0.05), f"Expected second frequency to be ~12.0, got {freqs[1]}."

    weights = data.get("weights_chunk_0", [])
    assert len(weights) == 5, f"Expected exactly 5 weights for the model, got {len(weights)}."

    # Expected weights based on the SVD of chunk 0 (rows 0-249) with seed 42 noise
    expected_weights = [4.981, 2.016, -1.500, -0.012, 2.992]

    for i, (act, exp) in enumerate(zip(weights, expected_weights)):
        assert math.isclose(act, exp, abs_tol=0.05), (
            f"Weight at index {i} mismatch. Expected ~{exp}, got {act}. "
            "Ensure you are using the correct chunk (rows 0-249) and SVD logic."
        )