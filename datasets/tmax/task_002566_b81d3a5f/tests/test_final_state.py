# test_final_state.py

import os
import csv
import pytest

def test_valid_models_file_exists():
    """Check if the output file valid_models.csv exists."""
    output_path = "/home/user/valid_models.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_valid_models_content():
    """Check if the output file contains the correct headers and sorted data."""
    output_path = "/home/user/valid_models.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The output file is empty."

    # Check headers
    headers = rows[0]
    assert headers == ["model_name", "mse"], f"Headers are incorrect. Expected ['model_name', 'mse'], got {headers}."

    # Check data rows
    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected exactly 3 valid models, got {len(data_rows)}."

    expected_data = [
        ["model_D", "0.0025"],
        ["model_A", "0.0200"],
        ["model_B", "0.2500"]
    ]

    for i, (expected_name, expected_mse) in enumerate(expected_data):
        actual_name, actual_mse = data_rows[i]
        assert actual_name == expected_name, f"Row {i+1}: Expected model_name '{expected_name}', got '{actual_name}'."
        assert actual_mse == expected_mse, f"Row {i+1}: Expected mse '{expected_mse}', got '{actual_mse}'."