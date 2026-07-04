# test_final_state.py

import os
import csv
import pytest

def test_projected_csv_correctness():
    input_path = "/home/user/data/measurements.csv"
    output_path = "/home/user/projected.csv"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did you run the Rust program?"

    # Read and process the input data to derive the expected truth
    valid_rows = []
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            try:
                id_val = row[0]
                features = [float(x) for x in row[1:]]
                valid_rows.append((id_val, features))
            except ValueError:
                # Skip rows with unparseable floats
                continue

    assert len(valid_rows) > 0, "No valid rows found in the input data."

    # Compute feature means
    num_features = len(valid_rows[0][1])
    means = [0.0] * num_features
    for _, features in valid_rows:
        for i in range(num_features):
            means[i] += features[i]
    for i in range(num_features):
        means[i] /= len(valid_rows)

    # Define the projection matrix from the task
    proj = [
        [0.5, 0.5, -0.5, -0.5],
        [0.5, -0.5, 0.5, -0.5]
    ]

    # Compute the expected projected rows
    expected_output = []
    for id_val, features in valid_rows:
        centered = [features[i] - means[i] for i in range(num_features)]
        p1 = sum(centered[i] * proj[0][i] for i in range(num_features))
        p2 = sum(centered[i] * proj[1][i] for i in range(num_features))
        expected_output.append((id_val, f"{p1:.4f}", f"{p2:.4f}"))

    # Read and validate the actual output
    actual_output = []
    with open(output_path, 'r') as f:
        reader = csv.reader(f)
        try:
            actual_header = next(reader)
        except StopIteration:
            pytest.fail(f"Output file {output_path} is empty.")

        assert actual_header == ["id", "p1", "p2"], f"Output header is incorrect. Expected ['id', 'p1', 'p2'], got {actual_header}"
        for row in reader:
            assert len(row) == 3, f"Row {row} does not have exactly 3 columns."
            actual_output.append((row[0], row[1], row[2]))

    assert len(actual_output) == len(expected_output), f"Output row count mismatch. Expected {len(expected_output)} rows, got {len(actual_output)}"

    for i, (expected, actual) in enumerate(zip(expected_output, actual_output)):
        assert expected == actual, f"Row {i+1} mismatch. Expected {expected}, got {actual}"