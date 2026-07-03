# test_final_state.py

import os
import pytest
import csv

COI_REPORT_PATH = '/home/user/coi_report.csv'
DEPT_STATS_PATH = '/home/user/dept_stats.csv'

def test_coi_report_exists_and_content():
    """Test that coi_report.csv exists and contains the correct data."""
    assert os.path.exists(COI_REPORT_PATH), f"Report file missing at {COI_REPORT_PATH}"
    assert os.path.isfile(COI_REPORT_PATH), f"{COI_REPORT_PATH} is not a file"

    expected_rows = [
        ['emp_id', 'department'],
        ['1', 'Executive'],
        ['6', 'SpecialOps'],
        ['7', 'IT'],
        ['8', 'IT']
    ]

    with open(COI_REPORT_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader if any(row)]  # ignore empty lines

    assert actual_rows == expected_rows, f"Content of {COI_REPORT_PATH} does not match expected output.\nExpected: {expected_rows}\nActual: {actual_rows}"

def test_dept_stats_exists_and_content():
    """Test that dept_stats.csv exists and contains the correct data."""
    assert os.path.exists(DEPT_STATS_PATH), f"Report file missing at {DEPT_STATS_PATH}"
    assert os.path.isfile(DEPT_STATS_PATH), f"{DEPT_STATS_PATH} is not a file"

    expected_rows = [
        ['department', 'coi_count', 'dept_rank'],
        ['IT', '2', '1'],
        ['Executive', '1', '2'],
        ['SpecialOps', '1', '2']
    ]

    with open(DEPT_STATS_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader if any(row)]  # ignore empty lines

    assert actual_rows == expected_rows, f"Content of {DEPT_STATS_PATH} does not match expected output.\nExpected: {expected_rows}\nActual: {actual_rows}"