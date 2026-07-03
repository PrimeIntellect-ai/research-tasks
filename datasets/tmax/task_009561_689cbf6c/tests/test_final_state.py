# test_final_state.py

import os
import csv

def test_scripts_exist():
    run_etl_path = '/home/user/run_etl.sh'
    process_py_path = '/home/user/process.py'

    assert os.path.exists(run_etl_path), f"Required script {run_etl_path} is missing."
    assert os.path.exists(process_py_path), f"Required script {process_py_path} is missing."

def test_filtered_data_log():
    filtered_path = '/home/user/filtered_data.log'
    assert os.path.exists(filtered_path), f"Intermediate file {filtered_path} is missing."

    with open(filtered_path, 'r') as f:
        content = f.read()

    assert "Status:ERROR" not in content, "filtered_data.log still contains 'Status:ERROR'"
    assert "Status:FAIL" not in content, "filtered_data.log still contains 'Status:FAIL'"
    assert "TRK-001" in content, "filtered_data.log seems to be missing valid lines."

def test_processed_csv():
    processed_path = '/home/user/processed.csv'
    assert os.path.exists(processed_path), f"Final output file {processed_path} is missing."

    with open(processed_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "processed.csv is empty."

    header = rows[0]
    expected_header = ['truck_id', 'timestamp', 'temperature']
    assert header == expected_header, f"Header row is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    expected_data = [
        ['TRK-001', '2023-10-01 10:00:00', '10.00'],
        ['TRK-001', '2023-10-01 10:05:00', '12.00'],
        ['TRK-001', '2023-10-01 10:10:00', '14.00'],
        ['TRK-001', '2023-10-01 10:15:00', '16.00'],
        ['TRK-002', '2023-10-01 11:00:00', '20.00'],
        ['TRK-002', '2023-10-01 11:05:00', '21.00'],
        ['TRK-002', '2023-10-01 11:10:00', '22.00'],
        ['TRK-003', '2023-10-01 12:00:00', '5.00'],
        ['TRK-003', '2023-10-01 12:05:00', '7.50'],
        ['TRK-003', '2023-10-01 12:10:00', '10.00'],
        ['TRK-003', '2023-10-01 12:15:00', '12.50'],
        ['TRK-003', '2023-10-01 12:20:00', '15.00']
    ]

    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, got {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."