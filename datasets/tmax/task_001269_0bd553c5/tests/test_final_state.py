# test_final_state.py
import json
import os
import pytest

def test_results_json_metric():
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), f"Output file {results_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not valid JSON.")

    assert isinstance(data, list), f"Expected a JSON array in {results_path}."

    agent_data = {}
    for item in data:
        assert isinstance(item, dict), "Each item in the array must be a JSON object."
        assert "root_name" in item, "Missing 'root_name' in item."
        assert "total_value" in item, "Missing 'total_value' in item."
        assert isinstance(item["total_value"], (int, float)), "'total_value' must be a number."
        agent_data[item["root_name"]] = item["total_value"]

    reference = {"Alpha": 100.5, "Beta": 45.2}

    agent_keys = set(agent_data.keys())
    ref_keys = set(reference.keys())

    assert agent_keys == ref_keys, f"Extracted target root nodes mismatch. Expected {ref_keys}, got {agent_keys}."

    mse = sum((agent_data[k] - reference[k])**2 for k in reference) / len(reference)

    assert mse <= 0.001, f"MSE of total_value is too high: {mse}. Expected <= 0.001."