# test_final_state.py

import os
import json
import pytest

def test_report_json_exists_and_correct():
    report_path = '/home/user/report.json'
    assert os.path.exists(report_path), f"The output file was not found at {report_path}. Did you save the report?"

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert isinstance(report_data, list), f"The JSON root in {report_path} must be an array (list)."

    expected_data = [
        {
            "emp1": "Alice",
            "emp2": "Bob",
            "weight": 5,
            "dept_name": "Engineering"
        },
        {
            "emp1": "Alice",
            "emp2": "Dave",
            "weight": 3,
            "dept_name": "Engineering"
        }
    ]

    # Sort both lists of dicts by emp1, emp2 to compare regardless of order
    try:
        sorted_report = sorted(report_data, key=lambda x: (x.get("emp1", ""), x.get("emp2", "")))
        sorted_expected = sorted(expected_data, key=lambda x: (x["emp1"], x["emp2"]))
    except TypeError:
        pytest.fail("The JSON output contains elements that are not comparable or missing expected string fields.")

    assert sorted_report == sorted_expected, (
        "The contents of the report.json do not match the expected output. "
        "Check if you correctly fixed the implicit cross join in the SQL query."
    )

def test_script_modified_to_save_json():
    script_path = '/home/user/generate_report.py'
    assert os.path.exists(script_path), f"Script file missing: {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    # We check if the script opens report.json for writing
    assert 'report.json' in content, "The script doesn't seem to reference 'report.json'."
    assert 'json.dump' in content or 'json.dumps' in content, "The script doesn't seem to use the json module to save the data."