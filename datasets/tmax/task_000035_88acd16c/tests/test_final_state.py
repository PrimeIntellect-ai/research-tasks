# test_final_state.py

import os
import pytest

def test_cleaned_csv_exists():
    """Check if cleaned.csv was generated."""
    assert os.path.isfile("/home/user/pipeline/cleaned.csv"), "File /home/user/pipeline/cleaned.csv does not exist. Did you run the Rust program?"

def test_cleaned_csv_content():
    """Check if cleaned.csv contains the correct processed data."""
    expected_lines = [
        "timestamp,distance",
        "1000,22.36",
        "1001,29.15",
        "1003,7.07"
    ]

    with open("/home/user/pipeline/cleaned.csv", "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in cleaned.csv, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual.strip()}'."