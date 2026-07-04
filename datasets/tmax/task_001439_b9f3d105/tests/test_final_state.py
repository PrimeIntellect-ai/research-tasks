# test_final_state.py

import os
import csv
import re
import pytest

def test_files_exist():
    assert os.path.exists('/home/user/process.py'), "process.py script is missing"
    assert os.path.exists('/home/user/cleaned_data.csv'), "cleaned_data.csv is missing"
    assert os.path.exists('/home/user/report.md'), "report.md is missing"

def test_report_content():
    report_path = '/home/user/report.md'
    if not os.path.exists(report_path):
        pytest.fail("report.md does not exist")

    with open(report_path, 'r', encoding='utf-8') as f:
        report = f.read()

    # Check for Average Temperatures
    assert "Average Temperature for Sensor A:" in report, "Missing Average Temperature for Sensor A in report"
    assert "Average Temperature for Sensor B:" in report, "Missing Average Temperature for Sensor B in report"

    # The expected averages are 21.85 for A and 22.31 for B
    assert "21.85" in report, "Incorrect Average Temperature for Sensor A (expected ~21.85)"
    assert "22.31" in report, "Incorrect Average Temperature for Sensor B (expected ~22.31)"

    # Check for similar log pairs
    pair_match_1 = '"Valve opened." and "Valve opened heavily!"' in report
    pair_match_2 = '"Valve opened heavily!" and "Valve opened."' in report
    assert pair_match_1 or pair_match_2, "Missing the expected similar log pair in the report"

    # Check similarity score (0.67 or 0.66 depending on rounding)
    assert "0.67" in report or "0.66" in report, "Missing or incorrect similarity score for the log pair (expected ~0.67)"

def test_cleaned_data_csv():
    csv_path = '/home/user/cleaned_data.csv'
    if not os.path.exists(csv_path):
        pytest.fail("cleaned_data.csv does not exist")

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 0, "cleaned_data.csv is empty"

    # Check headers
    headers = reader.fieldnames
    assert headers is not None, "cleaned_data.csv has no headers"

    required_columns = {'timestamp', 'sensor', 'temp', 'log'}
    assert required_columns.issubset(set(headers)), f"cleaned_data.csv is missing required columns. Found: {headers}"

    # Check if there are rows for both sensor A and B
    sensors = set(row['sensor'] for row in rows if 'sensor' in row)
    assert 'A' in sensors, "Sensor A data missing in cleaned_data.csv"
    assert 'B' in sensors, "Sensor B data missing in cleaned_data.csv"