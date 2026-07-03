# test_final_state.py

import os
import pytest

def test_best_k_file():
    """Check if best_k.txt contains the correct optimal k value."""
    path = "/home/user/best_k.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "8", f"Expected best_k.txt to contain '8', but got '{content}'."

def test_cleaned_data_file():
    """Verify that cleaned_data.csv is correctly generated with k=8."""
    input_path = "/home/user/sensor_data.csv"
    output_path = "/home/user/cleaned_data.csv"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(input_path, 'r') as f:
        input_lines = f.read().strip().split('\n')

    expected_lines = []
    k = 8
    for line in input_lines:
        if not line.strip():
            continue
        parts = line.strip().split(',')
        features = [float(x) for x in parts[:-1]]
        label = int(float(parts[-1]))

        reduced = []
        for i in range(0, len(features), k):
            chunk = features[i:i+k]
            reduced.append(sum(chunk) / k)

        formatted_reduced = [f"{val:.4f}" for val in reduced]
        expected_line = ",".join(formatted_reduced) + f",{label}"
        expected_lines.append(expected_line)

    with open(output_path, 'r') as f:
        output_lines = f.read().strip().split('\n')

    assert len(output_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in cleaned_data.csv, but found {len(output_lines)}."

    for i, (out_line, exp_line) in enumerate(zip(output_lines, expected_lines)):
        assert out_line.strip() == exp_line, f"Mismatch at row {i+1} in cleaned_data.csv.\nExpected: {exp_line}\nGot:      {out_line.strip()}"