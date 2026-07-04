# test_final_state.py
import os
import csv
import pytest

def test_analyze_script_exists():
    """Verify that the analyze.py script exists."""
    script_path = '/home/user/analyze.py'
    assert os.path.isfile(script_path), f"Python script missing at {script_path}"

def test_csv_output_exists():
    """Verify that the top_growth.csv file exists."""
    csv_path = '/home/user/top_growth.csv'
    assert os.path.isfile(csv_path), f"Output CSV missing at {csv_path}"

def test_csv_content():
    """Verify that the CSV output contains the correct data and schema."""
    csv_path = '/home/user/top_growth.csv'

    expected_data = [
        {"climate_zone": "Temperate", "species": "Pine", "date": "2023-01-02", "daily_growth": 5, "rolling_health": 5.5},
        {"climate_zone": "Temperate", "species": "Oak", "date": "2023-01-03", "daily_growth": 3, "rolling_health": 9.0},
        {"climate_zone": "Tropical", "species": "Palm", "date": "2023-01-03", "daily_growth": 6, "rolling_health": 9.0},
        {"climate_zone": "Tropical", "species": "Palm", "date": "2023-01-02", "daily_growth": 4, "rolling_health": 9.5},
    ]

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Check headers
    expected_headers = ["climate_zone", "species", "date", "daily_growth", "rolling_health"]
    assert reader.fieldnames == expected_headers, f"Expected headers {expected_headers}, got {reader.fieldnames}"

    # Check row count
    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows of data, got {len(rows)}"

    # Check row values
    for i, (expected, actual) in enumerate(zip(expected_data, rows)):
        assert actual["climate_zone"] == expected["climate_zone"], f"Row {i+1}: Expected climate_zone {expected['climate_zone']}, got {actual['climate_zone']}"
        assert actual["species"] == expected["species"], f"Row {i+1}: Expected species {expected['species']}, got {actual['species']}"
        assert actual["date"] == expected["date"], f"Row {i+1}: Expected date {expected['date']}, got {actual['date']}"

        try:
            actual_growth = int(actual["daily_growth"])
        except ValueError:
            pytest.fail(f"Row {i+1}: daily_growth '{actual['daily_growth']}' is not a valid integer")
        assert actual_growth == expected["daily_growth"], f"Row {i+1}: Expected daily_growth {expected['daily_growth']}, got {actual_growth}"

        try:
            actual_health = float(actual["rolling_health"])
        except ValueError:
            pytest.fail(f"Row {i+1}: rolling_health '{actual['rolling_health']}' is not a valid float")
        assert actual_health == expected["rolling_health"], f"Row {i+1}: Expected rolling_health {expected['rolling_health']}, got {actual_health}"