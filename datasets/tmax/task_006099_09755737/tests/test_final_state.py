# test_final_state.py

import os
import csv
import pytest

OUTPUT_FILE = "/home/user/sensor_risk_report.csv"
INPUT_FILE = "/home/user/sensor_data.csv"

def test_output_file_exists():
    """Test that the output report file was created."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} was not found."

def test_output_file_format_and_values():
    """Test the content, formatting, and calculations of the output report."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} was not found."

    with open(OUTPUT_FILE, mode='r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The output CSV file is empty."

    # Check header
    expected_header = ['sensor_id', 'mean_temp', 'max_humidity', 'risk_score']
    assert rows[0] == expected_header, f"Expected header {expected_header}, but got {rows[0]}."

    # Check data rows
    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected 3 data rows, but found {len(data_rows)}."

    # Expected values are derived from the input data provided in the truth setup
    # S1: mean_temp=22.50, max_hum=47.50, score=61.75
    # S2: mean_temp=18.25, max_hum=62.00, score=66.98
    # S3: mean_temp=30.25, max_hum=35.00, score=63.38
    expected_data = [
        ['S1', '22.50', '47.50', '61.75'],
        ['S2', '18.25', '62.00', '66.98'],
        ['S3', '30.25', '35.00', '63.38']
    ]

    # Check sorting by sensor_id
    sensor_ids = [row[0] for row in data_rows]
    assert sensor_ids == ['S1', 'S2', 'S3'], f"Rows must be sorted by sensor_id. Got {sensor_ids}."

    for i, (actual_row, expected_row) in enumerate(zip(data_rows, expected_data)):
        assert len(actual_row) == 4, f"Row {i+1} does not have exactly 4 columns: {actual_row}"

        sensor_id, mean_temp, max_humidity, risk_score = actual_row
        exp_id, exp_temp, exp_hum, exp_score = expected_row

        assert sensor_id == exp_id, f"Row {i+1}: Expected sensor_id '{exp_id}', got '{sensor_id}'."

        # Check numerical values and 2 decimal places formatting
        for val_name, actual_val, exp_val in [
            ('mean_temp', mean_temp, exp_temp),
            ('max_humidity', max_humidity, exp_hum),
            ('risk_score', risk_score, exp_score)
        ]:
            try:
                float_val = float(actual_val)
            except ValueError:
                pytest.fail(f"Row {i+1}: {val_name} '{actual_val}' is not a valid number.")

            # The task requires exactly 2 decimal places in the output
            # Some libraries might output e.g. "22.5" instead of "22.50". We check numerical equality first,
            # and optionally string formatting if strictness is required.
            assert abs(float_val - float(exp_val)) < 0.015, \
                f"Row {i+1}: Expected {val_name} ~{exp_val}, got {actual_val}."

            # Check if it has 2 decimal places
            parts = actual_val.split('.')
            assert len(parts) == 2 and len(parts[1]) == 2, \
                f"Row {i+1}: {val_name} '{actual_val}' is not rounded to exactly 2 decimal places."