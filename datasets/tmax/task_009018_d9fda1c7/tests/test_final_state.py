# test_final_state.py
import os
import csv

def test_summary_csv_exists_and_correct():
    csv_path = '/home/user/summary.csv'
    assert os.path.isfile(csv_path), f"Expected output file {csv_path} does not exist."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The summary.csv file is empty."

    header = rows[0]
    expected_header = ['sensor', 'avg_temp', 'avg_humidity']
    assert header == expected_header, f"Expected header {expected_header}, but got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected 3 data rows, but got {len(data_rows)}."

    expected_data = [
        ['Alpha', '21.00', '47.50'],
        ['Beta', '25.50', '47.50'],
        ['Delta', '10.00', '50.00']
    ]

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, but got {actual}."

    # Verify sorting
    sensors = [row[0] for row in data_rows]
    assert sensors == sorted(sensors), "Rows are not sorted alphabetically by the sensor name."