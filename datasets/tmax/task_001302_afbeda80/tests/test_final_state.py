# test_final_state.py

import os
import csv
import pytest

def test_processed_data_csv():
    path = '/home/user/processed_data.csv'
    assert os.path.isfile(path), f"File {path} is missing. Did you save the processed data?"

    expected_rows = [
        ['device_id', 'timestamp', 'anomaly_prob'],
        ['D1', '1', '0.4061'],
        ['D1', '2', '0.4256'],
        ['D1', '3', '0.4651'],
        ['D1', '4', '0.5112'],
        ['D2', '1', '0.4158'],
        ['D2', '2', '0.4061'],
        ['D2', '3', '0.3682'],
        ['D2', '4', '0.4576']
    ]

    with open(path, 'r') as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader if row]

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in {path}, but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

def test_heatmap_png_generated():
    path = '/home/user/heatmap.png'
    assert os.path.isfile(path), f"File {path} is missing. Did you fix and run the plotting script?"

    with open(path, 'rb') as f:
        header = f.read(4)

    assert header == b'\x89PNG', f"File {path} is not a valid PNG image."