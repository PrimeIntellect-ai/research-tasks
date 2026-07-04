# test_final_state.py

import os
import pytest

def test_makefile_exists():
    assert os.path.isfile("/home/user/Makefile"), "Makefile is missing."

def test_go_code_exists():
    assert os.path.isfile("/home/user/analyze.go"), "analyze.go is missing."

def test_pipeline_output_exists():
    assert os.path.isfile("/home/user/pipeline_output.tsv"), "pipeline_output.tsv is missing."

def test_pipeline_output_content():
    output_path = "/home/user/pipeline_output.tsv"
    scores_path = "/home/user/sequence_scores.txt"

    assert os.path.isfile(output_path), f"Missing {output_path}"
    assert os.path.isfile(scores_path), f"Missing {scores_path}"

    with open(scores_path, "r") as f:
        scores = [float(line.strip()) for line in f if line.strip()]

    assert len(scores) == 1000, "Expected 1000 scores in sequence_scores.txt"

    with open(output_path, "r") as f:
        lines = [line.strip().split('\t') for line in f if line.strip()]

    assert len(lines) > 0, "pipeline_output.tsv is empty"
    header = lines[0]
    expected_header = ["Start", "End", "Mean", "Lower95", "Upper95"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    data_rows = lines[1:]

    expected_starts = [0, 100, 200, 250, 300, 400, 500, 550, 600, 700, 800, 850, 900]
    expected_ends = [100, 200, 250, 300, 400, 500, 550, 600, 700, 800, 850, 900, 1000]

    assert len(data_rows) == len(expected_starts), f"Expected {len(expected_starts)} rows, got {len(data_rows)}"

    for i, row in enumerate(data_rows):
        assert len(row) == 5, f"Row {i+1} does not have exactly 5 columns"

        start = int(row[0])
        end = int(row[1])
        mean_val = float(row[2])
        lower = float(row[3])
        upper = float(row[4])

        assert start == expected_starts[i], f"Row {i+1}: expected Start {expected_starts[i]}, got {start}"
        assert end == expected_ends[i], f"Row {i+1}: expected End {expected_ends[i]}, got {end}"

        # Calculate expected mean
        bin_scores = scores[start:end]
        expected_mean = sum(bin_scores) / len(bin_scores)

        assert abs(mean_val - expected_mean) < 1e-3, f"Row {i+1}: expected Mean ~{expected_mean:.4f}, got {mean_val}"
        assert lower <= upper, f"Row {i+1}: Lower95 ({lower}) is greater than Upper95 ({upper})"
        # Bootstrap CI typically contains the sample mean, or is very close
        assert lower - 0.1 <= mean_val <= upper + 0.1, f"Row {i+1}: Mean {mean_val} is far outside CI [{lower}, {upper}]"