# test_final_state.py

import os
import json
import csv
import pytest

CSV_PATH = '/home/user/optimal_path.csv'
JSON_PATH = '/home/user/path_summary.json'
QUERY_PLAN_PATH = '/home/user/query_plan.txt'

def test_optimal_path_csv():
    """Verify that optimal_path.csv exists and has the correct content."""
    assert os.path.exists(CSV_PATH), f"CSV file not found at {CSV_PATH}"

    expected_rows = [
        ['step_number', 'location_name', 'cumulative_cost'],
        ['1', 'Alpha_Manufacturing', '0'],
        ['2', 'Beta_Hub', '10'],
        ['3', 'Gamma_Depot', '25'],
        ['4', 'Omega_Distribution', '45']
    ]

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader if row] # ignore empty lines

    assert actual_rows == expected_rows, f"CSV content does not match expected output. Actual: {actual_rows}"

def test_path_summary_json():
    """Verify that path_summary.json exists and has the correct content."""
    assert os.path.exists(JSON_PATH), f"JSON file not found at {JSON_PATH}"

    expected_json = {
        "total_cost": 45,
        "hop_count": 3,
        "path": [
            "Alpha_Manufacturing",
            "Beta_Hub",
            "Gamma_Depot",
            "Omega_Distribution"
        ]
    }

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert actual_json == expected_json, f"JSON content does not match expected output. Actual: {actual_json}"

def test_query_plan():
    """Verify that query_plan.txt exists and is not empty."""
    assert os.path.exists(QUERY_PLAN_PATH), f"Query plan file not found at {QUERY_PLAN_PATH}"
    assert os.path.getsize(QUERY_PLAN_PATH) > 0, f"Query plan file {QUERY_PLAN_PATH} is empty"