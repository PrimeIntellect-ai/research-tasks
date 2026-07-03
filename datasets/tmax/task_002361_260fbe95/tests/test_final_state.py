# test_final_state.py
import os
import json

def test_bom_summary_json_exists():
    file_path = '/home/user/bom_summary.json'
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

def test_bom_summary_json_contents():
    file_path = '/home/user/bom_summary.json'
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    assert "total_cost" in data, "Key 'total_cost' missing from bom_summary.json"
    assert "max_depth" in data, "Key 'max_depth' missing from bom_summary.json"

    # Check total cost
    expected_cost = 170.0
    actual_cost = float(data["total_cost"])
    assert actual_cost == expected_cost, f"Expected total_cost to be {expected_cost}, but got {actual_cost}"

    # Check max depth
    expected_depth = 3
    actual_depth = int(data["max_depth"])
    assert actual_depth == expected_depth, f"Expected max_depth to be {expected_depth}, but got {actual_depth}"