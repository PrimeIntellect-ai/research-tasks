# test_final_state.py
import os
import csv

def test_pipeline_c_exists():
    """Verify that the user created the C source file."""
    filepath = "/home/user/pipeline.c"
    assert os.path.exists(filepath), f"The C source file {filepath} is missing. You must write your solution in C."

def test_predictions_csv_correct():
    """Verify that the predictions.csv file exists and contains the correct computed scores."""
    pred_path = "/home/user/predictions.csv"
    assert os.path.exists(pred_path), f"Output file not found: {pred_path}. Did you run your compiled program?"

    # Recompute or use the known truth based on the setup
    # The expected math derived from the initial files:
    # ID 1: f=[10, 20, 8, 4] -> PCA -> Score: -12.0
    # ID 2: f=[15, 25, 6, 3] -> PCA -> Score: -19.0
    # ID 3: f=[12, 22, 5, 2] -> PCA -> Score: -17.0

    expected_output = [
        "id,score",
        "1,-12.0",
        "2,-19.0",
        "3,-17.0"
    ]

    with open(pred_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) > 0, f"The file {pred_path} is empty."

    # Check header
    assert actual_lines[0] == expected_output[0], f"Incorrect header in {pred_path}. Expected 'id,score', got '{actual_lines[0]}'."

    # Check data rows
    assert len(actual_lines) == len(expected_output), f"Incorrect number of rows in {pred_path}. Expected {len(expected_output)}, got {len(actual_lines)}."

    for i in range(1, len(expected_output)):
        assert actual_lines[i] == expected_output[i], (
            f"Mismatch at row {i}. Expected '{expected_output[i]}', got '{actual_lines[i]}'. "
            "Check your data joining, matrix multiplication, or sorting logic."
        )