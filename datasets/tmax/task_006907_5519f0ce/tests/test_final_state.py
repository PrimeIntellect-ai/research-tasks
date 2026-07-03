# test_final_state.py

import os
import csv
import pytest

def test_pipeline_script_exists():
    script_path = "/home/user/pipeline.py"
    assert os.path.isfile(script_path), f"Pipeline script {script_path} does not exist."

def test_output_summary_exists_and_correct():
    output_path = "/home/user/output/summary.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Output file is empty."

    # Check header
    header = rows[0]
    assert header == ['Region', 'Total_Revenue'], f"Expected header ['Region', 'Total_Revenue'], got {header}"

    # Check data rows
    data = rows[1:]
    assert len(data) == 3, f"Expected 3 data rows, got {len(data)}"

    # Check contents and sorting
    expected_data = [
        ['EU', '3500.50'],
        ['UK', '4201.00'],
        ['US', '3500.50']
    ]

    for i, expected_row in enumerate(expected_data):
        assert data[i] == expected_row, f"Row {i+1} mismatch: expected {expected_row}, got {data[i]}"