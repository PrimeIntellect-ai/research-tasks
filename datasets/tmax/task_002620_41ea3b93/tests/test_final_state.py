# test_final_state.py
import os
import json
import pytest

def test_dept_metrics_exists():
    path = "/home/user/dept_metrics.json"
    assert os.path.exists(path), f"File {path} is missing. The script must generate this file."
    assert os.path.isfile(path), f"{path} should be a file."

def test_dept_metrics_content():
    path = "/home/user/dept_metrics.json"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert isinstance(data, list), f"The JSON in {path} must be an array of objects."
    assert len(data) == 3, f"Expected 3 departments in the output, found {len(data)}."

    expected_data = [
        {
            "department": "Engineering",
            "employee_count": 4,
            "avg_depth": 1.5
        },
        {
            "department": "HR",
            "employee_count": 1,
            "avg_depth": 1.0
        },
        {
            "department": "Sales",
            "employee_count": 2,
            "avg_depth": 1.5
        }
    ]

    # Check alphabetical order by department name
    departments = [item.get("department") for item in data]
    assert departments == ["Engineering", "HR", "Sales"], "The JSON output must be ordered alphabetically by department name."

    for i, expected in enumerate(expected_data):
        actual = data[i]
        assert actual.get("department") == expected["department"], f"Expected department {expected['department']}, got {actual.get('department')}."
        assert actual.get("employee_count") == expected["employee_count"], f"Incorrect employee_count for {expected['department']}."

        # Float comparison for avg_depth
        actual_depth = actual.get("avg_depth")
        assert actual_depth is not None, f"Missing avg_depth for {expected['department']}."
        assert isinstance(actual_depth, (int, float)), f"avg_depth for {expected['department']} must be a number."
        assert abs(float(actual_depth) - expected["avg_depth"]) < 0.01, f"Incorrect avg_depth for {expected['department']}. Expected {expected['avg_depth']}, got {actual_depth}."