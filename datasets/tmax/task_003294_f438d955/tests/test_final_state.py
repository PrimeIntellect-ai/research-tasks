# test_final_state.py

import os
import csv
import pytest

def test_final_metrics_exists_and_correct():
    """Test that the final sorted metrics CSV is generated correctly."""
    file_path = "/home/user/final_metrics.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 4, f"Expected at least 4 rows in {file_path} (including header), found {len(rows)}."

    headers = rows[0]
    expected_headers = ["product_id", "total_upvotes", "total_emojis", "avg_char_count"]
    assert headers == expected_headers, f"Headers in {file_path} do not match. Expected {expected_headers}, got {headers}."

    expected_data = [
        {"product_id": "PROD_A", "total_upvotes": 45, "total_emojis": 3, "avg_char_count": 19.0},
        {"product_id": "PROD_C", "total_upvotes": 35, "total_emojis": 3, "avg_char_count": 18.33},
        {"product_id": "PROD_B", "total_upvotes": 10, "total_emojis": 2, "avg_char_count": 14.5},
    ]

    for i, expected in enumerate(expected_data):
        actual_row = rows[i+1]
        assert actual_row[0] == expected["product_id"], f"Row {i+1} product_id mismatch. Expected {expected['product_id']}, got {actual_row[0]}."
        assert int(actual_row[1]) == expected["total_upvotes"], f"Row {i+1} total_upvotes mismatch. Expected {expected['total_upvotes']}, got {actual_row[1]}."
        assert int(actual_row[2]) == expected["total_emojis"], f"Row {i+1} total_emojis mismatch. Expected {expected['total_emojis']}, got {actual_row[2]}."
        assert abs(float(actual_row[3]) - expected["avg_char_count"]) < 0.01, f"Row {i+1} avg_char_count mismatch. Expected {expected['avg_char_count']}, got {actual_row[3]}."

def test_scripts_exist():
    """Test that the required Python scripts were created."""
    expected_scripts = [
        "/home/user/extract.py",
        "/home/user/aggregate.py",
        "/home/user/sort.py",
        "/home/user/pipeline.py"
    ]
    for script in expected_scripts:
        assert os.path.isfile(script), f"Required script {script} is missing."