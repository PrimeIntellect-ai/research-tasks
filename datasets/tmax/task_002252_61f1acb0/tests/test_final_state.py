# test_final_state.py

import os
import pytest

def test_predictions_csv_exists_and_correct():
    filepath = '/home/user/predictions.csv'
    assert os.path.isfile(filepath), f"Output file {filepath} is missing. The script did not generate the required output."

    with open(filepath, 'r') as f:
        content = f.read().strip().split('\n')

    expected_content = [
        "id,predicted_label",
        "4,A",
        "5,B",
        "7,A",
        "11,A"
    ]

    assert len(content) == len(expected_content), f"Expected {len(expected_content)} rows in {filepath}, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_content)):
        assert actual.strip() == expected, f"Row {i+1} in {filepath} is incorrect. Expected '{expected}', got '{actual.strip()}'."