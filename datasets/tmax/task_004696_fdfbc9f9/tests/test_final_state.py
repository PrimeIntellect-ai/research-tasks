# test_final_state.py

import os
import csv
import pytest

def test_features_csv_exists():
    path = "/home/user/features.csv"
    assert os.path.isfile(path), f"{path} does not exist. Did you run the Rust program?"

def test_features_csv_content():
    path = "/home/user/features.csv"

    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "features.csv is empty"

        expected_header = ["node_id", "degree", "dominant_freq_index", "ci_lower", "ci_upper"]
        assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

        rows = list(reader)

    assert len(rows) == 4, f"Expected exactly 4 data rows, found {len(rows)}"

    expected_degrees = {0: 2, 1: 3, 2: 2, 3: 1}
    expected_freqs = {0: 2, 1: 3, 2: 4, 3: 5}

    for i, row in enumerate(rows):
        assert len(row) == 5, f"Row {i} does not have exactly 5 columns"

        node_id = int(row[0])
        assert node_id == i, f"Expected node_id {i} at row {i}, found {node_id}. Rows must be sorted by node_id ascending."

        degree = int(row[1])
        assert degree == expected_degrees[node_id], f"Node {node_id}: expected degree {expected_degrees[node_id]}, got {degree}"

        freq = int(row[2])
        assert freq == expected_freqs[node_id], f"Node {node_id}: expected dominant_freq_index {expected_freqs[node_id]}, got {freq}"

        ci_lower = float(row[3])
        ci_upper = float(row[4])

        assert ci_lower < ci_upper, f"Node {node_id}: ci_lower ({ci_lower}) must be strictly less than ci_upper ({ci_upper})"

        # The true mean of the sine wave over exactly integer periods is 0.
        # The noise is Gaussian with mean 0 and stddev 0.5.
        # The sample mean over 128 points should be close to 0.
        # The 95% CI should generally contain or be near 0, and bounds shouldn't be extreme.
        assert -1.0 <= ci_lower <= 1.0, f"Node {node_id}: ci_lower ({ci_lower}) is outside reasonable bounds"
        assert -1.0 <= ci_upper <= 1.0, f"Node {node_id}: ci_upper ({ci_upper}) is outside reasonable bounds"