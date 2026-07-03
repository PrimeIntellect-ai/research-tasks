# test_final_state.py

import os
import pytest

def test_executable_exists():
    executable = "/home/user/prepare_data"
    assert os.path.isfile(executable), f"Executable not found at {executable}. Did you compile the C++ script?"
    assert os.access(executable, os.X_OK), f"File at {executable} is not executable."

def test_features_output():
    features_output = "/home/user/features_output.csv"
    assert os.path.isfile(features_output), f"Output file not found at {features_output}. Did you run the executable?"

    with open(features_output, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 6, f"Expected 6 lines in {features_output} (1 header + 5 rows), found {len(lines)}"
    assert lines[0] == "x,f1,f2,y_pred", "Header in features_output.csv is incorrect"

    # Validate specific rows to ensure the math is correct
    # C++ default float formatting might omit trailing zeros, e.g., "1,0.2,0.04,1.08"
    assert "1,0.2,0.04,1.08" in lines[1], f"Row 1 incorrect. Expected '1,0.2,0.04,1.08', got '{lines[1]}'"
    assert "2,0.4,0.16,2.32" in lines[2], f"Row 2 incorrect. Expected '2,0.4,0.16,2.32', got '{lines[2]}'"
    assert "3,0.6,0.36,3.72" in lines[3], f"Row 3 incorrect. Expected '3,0.6,0.36,3.72', got '{lines[3]}'"
    assert "4,0.8,0.64,5.28" in lines[4], f"Row 4 incorrect. Expected '4,0.8,0.64,5.28', got '{lines[4]}'"
    assert "5,1,1,7" in lines[5], f"Row 5 incorrect. Expected '5,1,1,7', got '{lines[5]}'"

def test_mse_output():
    mse_output = "/home/user/mse.txt"
    assert os.path.isfile(mse_output), f"Output file not found at {mse_output}. Did you run the executable?"

    with open(mse_output, 'r') as f:
        content = f.read().strip()

    # The MSE should evaluate to exactly 0 (or 0.0) since predictions perfectly match the labels
    assert content.startswith("MSE:"), "mse.txt does not start with 'MSE:'"

    # Extract the value
    try:
        mse_value = float(content.split("MSE:")[1].strip())
    except ValueError:
        pytest.fail(f"Could not parse a float value from mse.txt content: '{content}'")

    assert mse_value == 0.0, f"Expected MSE to be 0.0, but got {mse_value}. The bug in the C++ script might not be fully fixed."