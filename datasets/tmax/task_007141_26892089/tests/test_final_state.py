# test_final_state.py

import os
import json
import csv
import pytest

def test_experiment_metrics_json():
    path = "/home/user/experiment_metrics.json"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the Rust program?"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON.")

    assert "vocab_size" in data, f"'vocab_size' key missing in {path}."
    assert "total_tokens" in data, f"'total_tokens' key missing in {path}."

    assert data["vocab_size"] == 9, f"Expected vocab_size to be 9, got {data['vocab_size']}."
    assert data["total_tokens"] == 12, f"Expected total_tokens to be 12, got {data['total_tokens']}."

def test_top_tokens_csv():
    path = "/home/user/top_tokens.csv"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the Rust program?"

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{path} is empty."

    header = rows[0]
    assert header == ["token", "probability"], f"Expected header ['token', 'probability'], got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected exactly 3 data rows in {path}, got {len(data_rows)}."

    expected_rows = [
        ["the", "0.190476"],
        ["dog", "0.142857"],
        ["barks", "0.095238"]
    ]

    for i, (expected, actual) in enumerate(zip(expected_rows, data_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."