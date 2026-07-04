# test_final_state.py
import os
import csv
import pytest

def test_inference_time_file():
    """Verify that inference_time.txt exists and contains a valid float."""
    file_path = "/home/user/inference_time.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content, f"File {file_path} is empty."

    try:
        time_val = float(content)
    except ValueError:
        pytest.fail(f"Content of {file_path} ('{content}') cannot be converted to a float.")

    assert time_val >= 0, f"Inference time in {file_path} must be non-negative."

def test_recommendations_file():
    """Verify that recommendations.csv exists and contains the correct recommendations."""
    file_path = "/home/user/recommendations.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    expected_rows = [
        ["original_product_id", "recommended_product_id"],
        ["p101", "p102"],
        ["p105", "p106"],
        ["p107", "p108"]
    ]

    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, f"Content of {file_path} does not match expected output.\nExpected: {expected_rows}\nActual: {actual_rows}"