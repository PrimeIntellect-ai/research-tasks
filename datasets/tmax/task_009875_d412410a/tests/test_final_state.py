# test_final_state.py
import os
import json
import pytest

def test_json_file_exists():
    """Verify that the output JSON file was created."""
    assert os.path.isfile('/home/user/hierarchy_cost.json'), "The output JSON file /home/user/hierarchy_cost.json does not exist."

def test_json_content():
    """Verify the structure, sorting, and values of the output JSON."""
    with open('/home/user/hierarchy_cost.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/hierarchy_cost.json does not contain valid JSON.")

    expected = [
        {"employee_name": "Alice Smith", "level": 0, "total_asset_cost": 2000},
        {"employee_name": "Bob Jones", "level": 1, "total_asset_cost": 2000},
        {"employee_name": "Charlie Brown", "level": 1, "total_asset_cost": 1500},
        {"employee_name": "Diana Prince", "level": 2, "total_asset_cost": 2500},
        {"employee_name": "Fiona Gallagher", "level": 2, "total_asset_cost": 0},
        {"employee_name": "Evan Wright", "level": 3, "total_asset_cost": 1300}
    ]

    assert isinstance(data, list), "The JSON root must be a list (array)."
    assert len(data) == len(expected), f"Expected {len(expected)} records, but got {len(data)}."

    for i, (actual, exp) in enumerate(zip(data, expected)):
        assert "employee_name" in actual, f"Record at index {i} is missing 'employee_name'."
        assert "level" in actual, f"Record at index {i} is missing 'level'."
        assert "total_asset_cost" in actual, f"Record at index {i} is missing 'total_asset_cost'."

        assert actual["employee_name"] == exp["employee_name"], f"Expected employee_name '{exp['employee_name']}' at index {i}, but got '{actual['employee_name']}'."
        assert actual["level"] == exp["level"], f"Expected level {exp['level']} for {exp['employee_name']}, but got {actual['level']}."
        assert float(actual["total_asset_cost"]) == float(exp["total_asset_cost"]), f"Expected total_asset_cost {exp['total_asset_cost']} for {exp['employee_name']}, but got {actual['total_asset_cost']}."

def test_script_exists_and_contains_logic():
    """Check if the python script exists and contains expected keywords for the required logic."""
    script_path = '/home/user/etl_hierarchy.py'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read().lower()

    assert "recursive" in content, "The script does not seem to use a Recursive CTE (missing 'RECURSIVE' keyword)."
    assert "manager-name" in content or "manager_name" in content, "The script does not seem to define the --manager-name argument."