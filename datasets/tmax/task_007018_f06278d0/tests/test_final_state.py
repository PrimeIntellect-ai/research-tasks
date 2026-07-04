# test_final_state.py

import os
import json
import pytest

def test_c_source_exists():
    assert os.path.isfile('/home/user/analyze.c'), "The C source file /home/user/analyze.c is missing."

def test_results_json_exists():
    assert os.path.isfile('/home/user/results.json'), "The results file /home/user/results.json is missing."

def test_results_json_content():
    results_path = '/home/user/results.json'

    try:
        with open(results_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail("The file /home/user/results.json does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read /home/user/results.json: {e}")

    expected_data = [
        {"concept": "DataScience", "out_degree": 2},
        {"concept": "NeuralNetworks", "out_degree": 2},
        {"concept": "Statistics", "out_degree": 2}
    ]

    assert isinstance(data, list), "The JSON output should be a list of objects."
    assert len(data) == 3, f"Expected 3 items in the JSON array, but found {len(data)}."

    for i, expected_item in enumerate(expected_data):
        actual_item = data[i]
        assert isinstance(actual_item, dict), f"Item at index {i} is not a JSON object."
        assert actual_item.get("concept") == expected_item["concept"], f"Expected concept '{expected_item['concept']}' at index {i}, got '{actual_item.get('concept')}'."
        assert actual_item.get("out_degree") == expected_item["out_degree"], f"Expected out_degree {expected_item['out_degree']} for concept '{expected_item['concept']}', got {actual_item.get('out_degree')}."