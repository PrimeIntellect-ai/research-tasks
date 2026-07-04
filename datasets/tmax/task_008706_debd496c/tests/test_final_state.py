# test_final_state.py

import os
import json
import csv
import sqlite3
import math
import pytest

def test_database_and_predictions():
    db_path = '/home/user/sensor_data.db'
    assert os.path.exists(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table schema
    cursor.execute("PRAGMA table_info(readings)")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    assert 'id' in columns, "Column 'id' missing in readings table."
    assert 'category' in columns, "Column 'category' missing in readings table."
    assert 'f1' in columns, "Column 'f1' missing in readings table."
    assert 'f2' in columns, "Column 'f2' missing in readings table."
    assert 'f3' in columns, "Column 'f3' missing in readings table."
    assert 'prediction' in columns, "Column 'prediction' missing in readings table."

    # Read raw data to compute expected
    raw_csv = '/home/user/raw_data.csv'
    expected_rows = []
    with open(raw_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['f1'] == '' or row['f2'] == '' or row['f3'] == '':
                continue
            expected_rows.append({
                'id': int(row['id']),
                'category': row['category'],
                'f1': float(row['f1']),
                'f2': float(row['f2']),
                'f3': float(row['f3'])
            })

    # Read weights
    weights_path = '/home/user/weights.json'
    with open(weights_path, 'r') as f:
        w = json.load(f)

    W1 = w['W1']
    b1 = w['b1']
    W2 = w['W2']
    b2 = w['b2']

    cursor.execute("SELECT id, category, f1, f2, f3, prediction FROM readings ORDER BY id")
    db_rows = cursor.fetchall()

    assert len(db_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in DB, got {len(db_rows)}"

    for db_row, exp_row in zip(db_rows, expected_rows):
        assert db_row[0] == exp_row['id']
        assert db_row[1] == exp_row['category']
        assert math.isclose(db_row[2], exp_row['f1'], rel_tol=1e-5)

        # Compute forward pass
        x = [exp_row['f1'], exp_row['f2'], exp_row['f3']]
        hidden = []
        for j in range(len(b1)):
            val = sum(x[i] * W1[i][j] for i in range(3)) + b1[j]
            hidden.append(max(0.0, val))

        pred = sum(hidden[j] * W2[j][0] for j in range(len(b2))) + b2[0]

        assert math.isclose(db_row[5], pred, rel_tol=1e-4), f"Prediction for id {db_row[0]} is incorrect. Expected {pred}, got {db_row[5]}"

    conn.close()

def test_summary_json():
    summary_path = '/home/user/summary.json'
    assert os.path.exists(summary_path), f"Summary file {summary_path} is missing."

    with open(summary_path, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json is not valid JSON")

    # Check that categories exist
    # Since we can't easily reproduce exact numpy bootstrap values in pure python,
    # we check the structure and ensure the bounds are reasonable floats.
    assert isinstance(summary, dict), "Summary should be a dictionary"

    for cat, bounds in summary.items():
        assert isinstance(bounds, list) and len(bounds) == 2, f"Bounds for {cat} should be a list of 2 elements"
        assert isinstance(bounds[0], (int, float)), "Lower bound must be a number"
        assert isinstance(bounds[1], (int, float)), "Upper bound must be a number"
        assert bounds[0] <= bounds[1], f"Lower bound {bounds[0]} is greater than upper bound {bounds[1]} for {cat}"