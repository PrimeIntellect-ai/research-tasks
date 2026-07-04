# test_final_state.py

import os
import json
import pytest

def test_audit_results_json():
    results_path = "/home/user/audit_results.json"
    assert os.path.exists(results_path), f"Expected results file {results_path} does not exist."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected a JSON list in {results_path}."
    assert len(data) == 1, f"Expected exactly 1 result in {results_path}, but found {len(data)}."

    record = data[0]
    assert "user_id" in record, "Result record is missing 'user_id' field."
    assert "total_accesses" in record, "Result record is missing 'total_accesses' field."

    assert record["user_id"] == "u001", f"Expected user_id 'u001', got {record['user_id']}."
    assert record["total_accesses"] == 3, f"Expected total_accesses 3, got {record['total_accesses']}."

def test_query_plan_json():
    plan_path = "/home/user/query_plan.json"
    assert os.path.exists(plan_path), f"Expected query plan file {plan_path} does not exist."
    assert os.path.isfile(plan_path), f"{plan_path} is not a file."

    with open(plan_path, 'r') as f:
        content = f.read()

    try:
        json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"File {plan_path} does not contain valid JSON.")

    content_lower = content.lower()
    assert "ixscan" in content_lower or "index" in content_lower, \
        "Query plan does not appear to use an index (missing 'IXSCAN' or 'index')."

def test_go_program_exists():
    go_script_path = "/home/user/audit.go"
    assert os.path.exists(go_script_path), f"Go program {go_script_path} does not exist."
    assert os.path.isfile(go_script_path), f"{go_script_path} is not a file."