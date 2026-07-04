# test_final_state.py

import os
import csv
import pytest

def test_pipeline_script_exists():
    """Verify that the user created the pipeline script."""
    pipeline_path = "/home/user/pipeline.py"
    assert os.path.isfile(pipeline_path), f"File {pipeline_path} is missing."

def test_predictions_csv_exists():
    """Verify that the predictions output file was generated."""
    predictions_path = "/home/user/predictions.csv"
    assert os.path.isfile(predictions_path), f"File {predictions_path} is missing."

def test_predictions_csv_content():
    """Verify the exact contents of the predictions file."""
    predictions_path = "/home/user/predictions.csv"

    expected_rows = [
        {"id": "8", "hash_key": "10_8", "prediction": "0"},
        {"id": "9", "hash_key": "-1_9", "prediction": "1"},
        {"id": "10", "hash_key": "20_10", "prediction": "1"},
        {"id": "11", "hash_key": "40_11", "prediction": "0"},
    ]

    with open(predictions_path, "r") as f:
        reader = csv.DictReader(f)

        # Check header
        expected_header = ["id", "hash_key", "prediction"]
        assert reader.fieldnames == expected_header, (
            f"Incorrect header in predictions.csv. Expected {expected_header}, got {reader.fieldnames}."
        )

        # Read all rows
        rows = list(reader)
        assert len(rows) == len(expected_rows), (
            f"Expected {len(expected_rows)} rows in predictions.csv, but got {len(rows)}."
        )

        # Check each row exactly
        for i, (expected, actual) in enumerate(zip(expected_rows, rows)):
            assert actual["id"] == expected["id"], (
                f"Row {i+1}: expected id '{expected['id']}', got '{actual['id']}'."
            )
            assert actual["hash_key"] == expected["hash_key"], (
                f"Row {i+1}: expected hash_key '{expected['hash_key']}', got '{actual['hash_key']}'. "
                "This usually indicates a failure to prevent pandas from converting missing values to floats."
            )
            assert actual["prediction"] == expected["prediction"], (
                f"Row {i+1}: expected prediction '{expected['prediction']}', got '{actual['prediction']}'. "
                "This indicates incorrect modeling, feature engineering, or random state initialization."
            )