# test_final_state.py

import os
import json
import pytest

def test_etl_output_exists():
    output_path = "/home/user/etl_output.json"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist. Did your script run successfully?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_etl_output_content():
    output_path = "/home/user/etl_output.json"
    assert os.path.exists(output_path), "Output file missing, cannot test content."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} does not contain valid JSON.")

    expected_keys = {"top_entity", "total_degree", "in_degree", "out_degree"}
    actual_keys = set(data.keys())

    assert actual_keys == expected_keys, f"JSON keys do not match exactly. Expected {expected_keys}, got {actual_keys}"

    assert data["top_entity"] == "U2", f"Expected top_entity to be 'U2', got '{data['top_entity']}'"
    assert data["total_degree"] == 5, f"Expected total_degree to be 5, got {data['total_degree']}"
    assert data["in_degree"] == 4, f"Expected in_degree to be 4, got {data['in_degree']}"
    assert data["out_degree"] == 1, f"Expected out_degree to be 1, got {data['out_degree']}"