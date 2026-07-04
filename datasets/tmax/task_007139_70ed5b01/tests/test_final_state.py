# test_final_state.py

import os
import json
import pytest

def test_files_exist():
    """Verify that all expected output files exist."""
    expected_files = [
        "/home/user/src/extract_matrices.cpp",
        "/home/user/data/matrices.json",
        "/home/user/analysis.ipynb",
        "/home/user/results.json"
    ]
    for path in expected_files:
        assert os.path.isfile(path), f"Expected file {path} is missing."

def test_matrices_json_structure():
    """Verify the structure and content of matrices.json."""
    path = "/home/user/data/matrices.json"
    with open(path, "r") as f:
        try:
            matrices = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not a valid JSON file.")

    expected_keys = {"Seq1", "Seq2", "Seq3"}
    assert set(matrices.keys()) == expected_keys, f"{path} keys do not match expected sequences."

    for seq, matrix in matrices.items():
        assert isinstance(matrix, list), f"Matrix for {seq} is not a list."
        assert len(matrix) == 4, f"Matrix for {seq} does not have 4 rows."
        for row in matrix:
            assert isinstance(row, list), f"Row in {seq} matrix is not a list."
            assert len(row) == 4, f"Row in {seq} matrix does not have 4 columns."

def test_results_json_content():
    """Verify the structure, bounds, and values in results.json."""
    path = "/home/user/results.json"
    with open(path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not a valid JSON file.")

    expected_keys = {"Seq1", "Seq2", "Seq3"}
    assert set(results.keys()) == expected_keys, f"{path} keys do not match expected sequences."

    expected_means = {
        "Seq1": 0.909,
        "Seq2": 0.909,
        "Seq3": 0.0
    }
    tolerance = 0.05

    for seq, data in results.items():
        for key in ["mean", "ci_lower", "ci_upper"]:
            assert key in data, f"Missing key '{key}' in {seq} results."
            assert isinstance(data[key], (int, float)), f"Value for '{key}' in {seq} is not numeric."

        mean = data["mean"]
        ci_lower = data["ci_lower"]
        ci_upper = data["ci_upper"]

        # Check CI validity
        assert ci_lower <= mean <= ci_upper, f"Confidence interval for {seq} is invalid: {ci_lower} <= {mean} <= {ci_upper} is False."

        # Check mean values
        expected_mean = expected_means[seq]
        assert abs(mean - expected_mean) <= tolerance, f"Mean for {seq} ({mean}) is not within {tolerance} of expected ({expected_mean})."