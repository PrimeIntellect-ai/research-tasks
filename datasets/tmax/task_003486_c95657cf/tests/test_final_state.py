# test_final_state.py
import os
import json
import pytest

SCRIPT_PATH = "/home/user/audit_graph.py"
OUTPUT_PATH = "/home/user/central_actors.json"

def test_script_exists_and_bypasses_index():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read().lower()
    assert "not indexed" in content, "The script does not seem to bypass the index using 'NOT INDEXED'."

def test_output_json_exists_and_format():
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} is not valid JSON.")

    assert isinstance(data, list), "JSON output should be a list."
    assert len(data) == 3, f"Expected exactly 3 items in the JSON output, found {len(data)}."

    for item in data:
        assert "employee_id" in item, "Missing 'employee_id' in JSON output."
        assert "centrality" in item, "Missing 'centrality' in JSON output."
        assert isinstance(item["centrality"], (int, float)), "Centrality must be a number."

def test_output_json_correct_actors():
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."
    with open(OUTPUT_PATH, 'r') as f:
        data = json.load(f)

    employee_ids = [item["employee_id"] for item in data]
    expected_ids = ["EMP999", "EMP888", "EMP777"]

    assert employee_ids == expected_ids, f"Expected top 3 actors to be {expected_ids}, but got {employee_ids}."