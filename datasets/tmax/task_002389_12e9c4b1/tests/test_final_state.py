# test_final_state.py

import os
import json
import pytest

def test_analyze_script_exists():
    script_path = '/home/user/analyze.sh'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_result_json_exists():
    result_path = '/home/user/result.json'
    assert os.path.isfile(result_path), f"The file {result_path} is missing."

def test_result_json_content():
    result_path = '/home/user/result.json'

    try:
        with open(result_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {result_path} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {result_path}: {e}")

    # Check total_salary_tree_E001
    assert "total_salary_tree_E001" in data, "The key 'total_salary_tree_E001' is missing from the JSON output."
    expected_salary = 40000
    actual_salary = data["total_salary_tree_E001"]
    assert actual_salary == expected_salary, f"Expected 'total_salary_tree_E001' to be {expected_salary}, but got {actual_salary}."

    # Check cross_dept_projects
    assert "cross_dept_projects" in data, "The key 'cross_dept_projects' is missing from the JSON output."
    expected_projects = ["P2", "P4"]
    actual_projects = data["cross_dept_projects"]
    assert isinstance(actual_projects, list), "The 'cross_dept_projects' value must be a JSON array."
    assert actual_projects == expected_projects, f"Expected 'cross_dept_projects' to be {expected_projects}, but got {actual_projects}."