# test_final_state.py

import os
import json
import pytest
import csv

def test_metrics_json_exists_and_valid():
    """Verify that metrics.json exists and contains the required keys."""
    file_path = "/home/user/metrics.json"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not a valid JSON file.")

    assert "accuracy" in metrics, f"'accuracy' key missing in {file_path}."
    assert "f1_score" in metrics, f"'f1_score' key missing in {file_path}."
    assert isinstance(metrics["accuracy"], (int, float)), "'accuracy' must be a number."
    assert isinstance(metrics["f1_score"], (int, float)), "'f1_score' must be a number."

def test_processed_events_csv_exists_and_valid():
    """Verify that processed_events.csv exists, has correct headers and no missing session_duration."""
    file_path = "/home/user/processed_events.csv"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"{file_path} is empty.")

        # Check for is_youth
        assert "is_youth" in headers, "Column 'is_youth' is missing from the processed CSV."

        # Check for integer one-hot encoded columns
        assert any(h.startswith("event_code_-1") and not h.startswith("event_code_-1.0") for h in headers), "event_code_-1 not found or formatted as float (e.g., event_code_-1.0)."
        assert any(h.startswith("event_code_4") and not h.startswith("event_code_4.0") for h in headers), "event_code_4 not found or formatted as float (e.g., event_code_4.0)."

        # Check that session_duration has no missing values
        assert "session_duration" in headers, "Column 'session_duration' is missing."
        session_duration_idx = headers.index("session_duration")

        for row_num, row in enumerate(reader, start=2):
            if len(row) > session_duration_idx:
                val = row[session_duration_idx].strip()
                assert val != "", f"Missing session_duration value found in row {row_num}."