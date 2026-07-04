# test_final_state.py

import os
import pytest

def test_fixed_mse_file():
    """Check if fixed_mse.txt exists and contains the correct MSE."""
    file_path = "/home/user/fixed_mse.txt"
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    # The expected MSE when correctly applying scaling after split
    expected_mse = "0.2476"
    assert content == expected_mse, f"Expected MSE to be {expected_mse}, but got {content}"

def test_predictions_file():
    """Check if predictions.txt exists and contains the correct first 10 predictions."""
    file_path = "/home/user/predictions.txt"
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 10, f"Expected exactly 10 predictions, but found {len(lines)}"

    # Expected predictions from the correctly fixed pipeline
    expected_preds = [
        "-18.7302",
        "208.5714",
        "-23.7317",
        "127.6698",
        "272.9348",
        "-22.1805",
        "55.3343",
        "54.8967",
        "-139.7925",
        "-292.0583"
    ]

    for i, (actual, expected) in enumerate(zip(lines, expected_preds)):
        assert actual == expected, f"Prediction at line {i+1} expected to be {expected}, but got {actual}"