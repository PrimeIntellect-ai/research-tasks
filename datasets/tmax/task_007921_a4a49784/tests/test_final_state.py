# test_final_state.py

import os
import csv
import pytest

def test_processed_logs_exists():
    """Check if the processed dataset exists."""
    output_path = "/home/user/processed_logs.csv"
    assert os.path.isfile(output_path), f"Output dataset {output_path} does not exist"

def test_processed_logs_content():
    """Check if the processed dataset has the correct content."""
    output_path = "/home/user/processed_logs.csv"
    assert os.path.isfile(output_path), f"Output dataset {output_path} does not exist"

    expected_rows = [
        {"id": "1", "safe_group_id": "100", "score": "0.2000"},
        {"id": "2", "safe_group_id": "-1", "score": "0.2000"},
        {"id": "3", "safe_group_id": "200", "score": "0.0000"},
        {"id": "4", "safe_group_id": "-1", "score": "-0.2000"},
        {"id": "5", "safe_group_id": "105", "score": "0.4000"},
    ]

    with open(output_path, "r") as f:
        reader = csv.DictReader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual.get("id") == expected["id"], f"Row {i+1}: expected id {expected['id']}, got {actual.get('id')}"
        assert actual.get("safe_group_id") == expected["safe_group_id"], f"Row {i+1}: expected safe_group_id {expected['safe_group_id']}, got {actual.get('safe_group_id')}"

        # Parse score as float to allow minor formatting differences if any, though exact match is preferred
        actual_score = actual.get("score")
        assert actual_score is not None, f"Row {i+1}: missing 'score' column"

        # Check exact string match as per requirement (formatted to 4 decimal places)
        assert actual_score == expected["score"], f"Row {i+1}: expected score {expected['score']}, got {actual_score}"

def test_cargo_toml_ndarray():
    """Check if ndarray is configured in Cargo.toml."""
    cargo_toml_path = "/home/user/log_pipeline/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"Cargo.toml does not exist at {cargo_toml_path}"

    with open(cargo_toml_path, "r") as f:
        content = f.read()

    assert "ndarray" in content, "The 'ndarray' crate is not configured in Cargo.toml"