# test_final_state.py

import os
import csv

def test_output_file_exists():
    """Check if the final output CSV file was created."""
    file_path = "/home/user/output/final_pipeline_output.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

def test_output_file_structure_and_types():
    """Check the structure, headers, row count, and data types of the output CSV."""
    file_path = "/home/user/output/final_pipeline_output.csv"

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("Output CSV is empty.")

        expected_header = ['timestamp', 'pca_0', 'pca_1', 'anomaly_score', 'is_anomaly']
        assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

        rows = list(reader)

        # 100 original rows - 2 dropped due to rolling window of 3 = 98 rows
        assert len(rows) == 98, f"Expected exactly 98 data rows, got {len(rows)}"

        for i, row in enumerate(rows):
            assert len(row) == 5, f"Row {i+1} has {len(row)} columns, expected 5."

            # timestamp should be a string (we don't strictly parse it here, just ensure it's not empty)
            assert row[0].strip(), f"Row {i+1} has an empty timestamp."

            # pca_0, pca_1, anomaly_score should be parseable as floats
            try:
                float(row[1])
            except ValueError:
                pytest.fail(f"Row {i+1}: pca_0 '{row[1]}' cannot be parsed as float.")

            try:
                float(row[2])
            except ValueError:
                pytest.fail(f"Row {i+1}: pca_1 '{row[2]}' cannot be parsed as float.")

            try:
                float(row[3])
            except ValueError:
                pytest.fail(f"Row {i+1}: anomaly_score '{row[3]}' cannot be parsed as float.")

            # is_anomaly should be 1 or -1
            # Allow for float representations like '1.0' or '-1.0' just in case pandas exported it that way
            assert row[4] in ['1', '-1', '1.0', '-1.0'], f"Row {i+1}: is_anomaly '{row[4]}' must be 1 or -1."