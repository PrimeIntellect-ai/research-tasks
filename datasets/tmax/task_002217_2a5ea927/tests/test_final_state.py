# test_final_state.py

import os
import json
import pytest

def test_summary_json_exists_and_correct():
    json_path = '/home/user/summary.json'
    assert os.path.exists(json_path), f"File {json_path} does not exist."
    assert os.path.isfile(json_path), f"{json_path} is not a regular file."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    assert "shortest_path" in data, "Key 'shortest_path' is missing in summary.json."
    expected_path = ["Alice Smith", "Charlie Brown", "David Lee", "Bob Jones"]
    assert data["shortest_path"] == expected_path, f"Expected shortest_path to be {expected_path}, got {data['shortest_path']}."

    assert "total_unique_papers" in data, "Key 'total_unique_papers' is missing in summary.json."
    assert data["total_unique_papers"] == 6, f"Expected total_unique_papers to be 6, got {data['total_unique_papers']}."

def test_query_plan_exists_and_valid():
    plan_path = '/home/user/query_plan.txt'
    assert os.path.exists(plan_path), f"File {plan_path} does not exist."
    assert os.path.isfile(plan_path), f"{plan_path} is not a regular file."

    with open(plan_path, 'r') as f:
        content = f.read().upper()

    assert "SCAN" in content or "SEARCH" in content, (
        f"{plan_path} does not seem to contain a valid SQLite execution plan "
        "(expected to find 'SCAN' or 'SEARCH' in the output)."
    )