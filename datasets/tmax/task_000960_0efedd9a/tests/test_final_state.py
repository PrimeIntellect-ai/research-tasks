# test_final_state.py

import os
import sqlite3
import pytest

def calculate_f1(pred_file, truth_file):
    try:
        with open(pred_file, 'r') as f:
            pred_ids = set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return 0.0

    with open(truth_file, 'r') as f:
        truth_ids = set(line.strip() for line in f if line.strip())

    if not pred_ids and not truth_ids:
        return 1.0
    if not pred_ids or not truth_ids:
        return 0.0

    tp = len(pred_ids.intersection(truth_ids))
    fp = len(pred_ids - truth_ids)
    fn = len(truth_ids - pred_ids)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)

def test_anomaly_f1_score():
    """Test that the F1 score of extracted anomaly IDs meets the threshold."""
    pred_file = '/home/user/anomaly_ids.txt'
    truth_file = '/app/.hidden_truth_ids.txt'

    assert os.path.exists(pred_file), f"Expected anomaly IDs file at {pred_file} does not exist."
    assert os.path.exists(truth_file), f"Hidden truth file at {truth_file} is missing."

    f1_score = calculate_f1(pred_file, truth_file)
    threshold = 0.95

    assert f1_score >= threshold, f"F1 Score {f1_score:.4f} is below the threshold of {threshold}."

def test_cleaned_csv_exists_and_format():
    """Test that the cleaned CSV file exists, has the right header, and row count."""
    csv_path = '/home/user/cleaned.csv'
    assert os.path.exists(csv_path), f"Cleaned CSV file at {csv_path} does not exist."

    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 1001, f"Expected 1001 lines in CSV (1 header + 1000 data rows), found {len(lines)}."
    assert lines[0].strip() == "id,timestamp,message,sensor_val", f"CSV header is incorrect. Found: {lines[0].strip()}"

    # Check that there are no missing values (forward fill applied)
    for i, line in enumerate(lines[1:], start=2):
        parts = line.strip().split(',')
        assert len(parts) >= 4, f"Line {i} in CSV does not have enough columns: {line.strip()}"
        assert parts[-1] != "" and parts[-1].lower() != "null" and parts[-1].lower() != "none", f"Missing sensor_val at line {i}: {line.strip()}"

def test_telemetry_db_exists_and_populated():
    """Test that the SQLite database exists and contains the logs table with data."""
    db_path = '/home/user/telemetry.db'
    assert os.path.exists(db_path), f"Database file at {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs'")
    table = cursor.fetchone()
    assert table is not None, "Table 'logs' does not exist in the database."

    cursor.execute("SELECT COUNT(*) FROM logs")
    count = cursor.fetchone()[0]
    assert count == 1000, f"Expected 1000 rows in 'logs' table, found {count}."

    conn.close()