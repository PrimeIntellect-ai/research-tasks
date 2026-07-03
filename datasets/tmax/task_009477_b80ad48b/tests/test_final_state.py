# test_final_state.py
import os
import json
import re

def test_audit_report_json():
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"Expected file {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a regular file."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not a valid JSON file."

    assert "unauthorized_accesses" in data, "JSON missing 'unauthorized_accesses' key."
    assert "index_strategy" in data, "JSON missing 'index_strategy' key."

    unauthorized = data["unauthorized_accesses"]
    assert isinstance(unauthorized, list), "'unauthorized_accesses' should be a list."
    assert len(unauthorized) == 3, f"Expected exactly 3 unauthorized accesses, got {len(unauthorized)}."

    expected_accesses = [
        {"employee_name": "Bob Jones", "department_name": "Sales"},
        {"employee_name": "Charlie Brown", "department_name": "Direct Sales"},
        {"employee_name": "Frank Miller", "department_name": "Operations"}
    ]

    # Verify the list is sorted by employee_name
    employee_names = [item.get("employee_name", "") for item in unauthorized]
    assert employee_names == sorted(employee_names), "'unauthorized_accesses' is not sorted alphabetically by employee_name."

    for expected in expected_accesses:
        assert expected in unauthorized, f"Expected entry {expected} not found in 'unauthorized_accesses'."

    # Check index strategy
    index_strategy = data["index_strategy"].strip()

    # Normalize whitespace and case for SQL keywords
    normalized_strategy = re.sub(r'\s+', ' ', index_strategy).upper()

    # However, table and column names should be precise.
    # We can check the exact string by replacing the known keywords to upper, or just match a regex.
    pattern = r"^CREATE\s+INDEX\s+idx_system_time\s+ON\s+access_logs\s*\(\s*system_name\s*,\s*access_time\s+DESC\s*\)\s*;?$"
    assert re.match(pattern, index_strategy, re.IGNORECASE), \
        f"Index strategy does not match the expected CREATE INDEX statement. Got: {index_strategy}"

    # Ensure table and column names are exact case
    assert "idx_system_time" in index_strategy, "Index name 'idx_system_time' not found with exact case."
    assert "access_logs" in index_strategy, "Table name 'access_logs' not found with exact case."
    assert "system_name" in index_strategy, "Column name 'system_name' not found with exact case."
    assert "access_time" in index_strategy, "Column name 'access_time' not found with exact case."