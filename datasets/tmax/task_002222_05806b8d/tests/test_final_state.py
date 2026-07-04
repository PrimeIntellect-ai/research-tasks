# test_final_state.py

import os
import csv
import pytest

def test_processed_features_exists():
    file_path = "/home/user/processed_features.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_processed_features_format_and_shape():
    file_path = "/home/user/processed_features.csv"

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)

        assert header is not None, "The processed_features.csv file is empty."
        assert header == ['PC1', 'PC2'], f"Expected header ['PC1', 'PC2'], got {header}"

        row_count = 0
        for row in reader:
            row_count += 1
            assert len(row) == 2, f"Row {row_count} does not have exactly 2 columns."

            # Check if values are valid floats
            try:
                pc1 = float(row[0])
                pc2 = float(row[1])
            except ValueError:
                pytest.fail(f"Row {row_count} contains non-numeric values: {row}")

            # Check rounding to 4 decimal places
            # A value like "1.2345" has 4 chars after the dot
            for val_str in row:
                if '.' in val_str:
                    decimals = len(val_str.split('.')[1])
                    assert decimals <= 4, f"Value {val_str} in row {row_count} is not rounded to 4 decimal places."

        assert row_count == 10000, f"Expected exactly 10,000 data rows, got {row_count}"

def test_prepare_data_script_exists():
    script_path = "/home/user/prepare_data.py"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."