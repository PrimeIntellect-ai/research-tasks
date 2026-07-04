# test_final_state.py
import os
import json
import csv
import pytest

def test_clean_data_file():
    clean_path = '/home/user/clean_data.csv'
    assert os.path.isfile(clean_path), f"Cleaned data file is missing: {clean_path}"

    with open(clean_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"File {clean_path} is empty.")

        assert header == ["text", "label"], f"Expected header ['text', 'label'], got {header}"

        row_count = 0
        for row in reader:
            row_count += 1
            assert len(row) == 2, f"Row {row_count} does not have exactly 2 columns."
            text = row[0]
            assert "!" not in text, f"Punctuation '!' found in clean_data.csv at row {row_count}"
            assert "?" not in text, f"Punctuation '?' found in clean_data.csv at row {row_count}"
            assert text == text.lower(), f"Uppercase letters found in clean_data.csv at row {row_count}"

        assert row_count == 300, f"Expected 300 rows of data, found {row_count} in {clean_path}"

def test_metrics_json():
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"Metrics file is missing: {metrics_path}"

    with open(metrics_path, 'r', encoding='utf-8') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_path} does not contain valid JSON.")

    assert "accuracy" in metrics, f"Key 'accuracy' is missing from {metrics_path}"

    acc = metrics["accuracy"]
    assert isinstance(acc, float), f"Accuracy must be a float, got {type(acc).__name__}"

    # Expected accuracy based on the correct pipeline and seed
    expected_acc = 0.9555555555555556
    assert abs(acc - expected_acc) < 1e-5, f"Expected accuracy ~{expected_acc}, but got {acc}. The data leakage might not be correctly fixed, or hyperparameters were changed."