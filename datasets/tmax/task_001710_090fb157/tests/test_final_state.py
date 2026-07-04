# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_database_exists_and_populated():
    db_path = "/home/user/metrics.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    # Connect and check table
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM readings;")
        count = cursor.fetchone()[0]
        assert count > 0, "The 'readings' table exists but is empty."
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'readings' table in {db_path}: {e}")
    finally:
        conn.close()

def test_anomalies_f1_score():
    pred_path = "/home/user/anomalies.json"
    truth_path = "/app/truth_anomalies.json"

    assert os.path.exists(pred_path), f"Prediction file {pred_path} does not exist."
    assert os.path.exists(truth_path), f"Truth file {truth_path} does not exist."

    try:
        with open(pred_path, "r") as f:
            pred_data = json.load(f)
            assert isinstance(pred_data, list), "Anomalies JSON must be a list."
            pred = set(pred_data)
    except json.JSONDecodeError:
        pytest.fail(f"File {pred_path} is not valid JSON.")

    with open(truth_path, "r") as f:
        truth = set(json.load(f))

    tp = len(pred & truth)
    fp = len(pred - truth)
    fn = len(truth - pred)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.95, (
        f"F1 Score is {f1:.4f}, which is below the threshold of 0.95. "
        f"(Precision: {precision:.4f}, Recall: {recall:.4f})"
    )

def test_html_report_contains_correct_count():
    report_path = "/home/user/report.html"
    pred_path = "/home/user/anomalies.json"

    assert os.path.exists(report_path), f"Report file {report_path} does not exist."
    assert os.path.exists(pred_path), f"Prediction file {pred_path} does not exist."

    with open(pred_path, "r") as f:
        pred_data = json.load(f)

    expected_count = len(pred_data)
    expected_tag = f'<div id="anomaly-count">{expected_count}</div>'

    with open(report_path, "r") as f:
        html_content = f.read()

    assert expected_tag in html_content, (
        f"The expected tag '{expected_tag}' was not found in {report_path}. "
        f"Ensure the count exactly matches the number of anomalies in {pred_path}."
    )