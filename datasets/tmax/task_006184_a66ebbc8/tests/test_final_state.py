# test_final_state.py

import os
import pytest

def test_venv_exists():
    """Test that the virtual environment was created successfully."""
    venv_python = '/home/user/venv/bin/python'
    assert os.path.isfile(venv_python), f"Virtual environment Python executable not found at {venv_python}. Did you create the venv?"

def test_directories_exist():
    """Test that the required artifact directories exist."""
    expected_dirs = [
        '/home/user/artifacts/models',
        '/home/user/artifacts/metrics',
        '/home/user/artifacts/predictions'
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Required directory not found: {d}"

def test_model_exists():
    """Test that the best Ridge model was saved to the correct path."""
    model_path = '/home/user/artifacts/models/best_ridge.pkl'
    assert os.path.isfile(model_path), f"Model file not found at {model_path}"
    assert os.path.getsize(model_path) > 0, "Model file is empty."

def test_mse_file():
    """Test that the MSE file exists, contains a valid positive float, and is rounded to 4 decimal places."""
    mse_path = '/home/user/artifacts/metrics/mse.txt'
    assert os.path.isfile(mse_path), f"MSE metric file not found at {mse_path}"

    with open(mse_path, 'r') as f:
        content = f.read().strip()

    try:
        mse_val = float(content)
    except ValueError:
        pytest.fail(f"MSE file content '{content}' is not a valid float.")

    assert mse_val > 0, f"Expected MSE to be greater than 0, got {mse_val}"

    # Check rounding to 4 decimal places
    if '.' in content:
        decimals = len(content.split('.')[1])
        assert decimals <= 4, f"MSE should be rounded to 4 decimal places, got {decimals} decimal places in '{content}'"

def test_predictions_file():
    """Test that the predictions CSV is formatted correctly and contains the correct hold-out indices."""
    preds_path = '/home/user/artifacts/predictions/preds.csv'
    assert os.path.isfile(preds_path), f"Predictions CSV not found at {preds_path}"

    with open(preds_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 201, f"Expected 201 lines (1 header + 200 rows), got {len(lines)}"
    assert lines[0] == "index,prediction", f"Incorrect header in predictions CSV. Expected 'index,prediction', got '{lines[0]}'"

    for i, line in enumerate(lines[1:]):
        expected_index = 800 + i
        parts = line.split(',')
        assert len(parts) == 2, f"Line {i+2} does not have exactly 2 columns: '{line}'"

        idx_str, pred_str = parts
        assert idx_str == str(expected_index), f"Expected index {expected_index} at row {i+2}, got {idx_str}. Did you use shuffle=False and test_size=0.2?"

        try:
            float(pred_str)
        except ValueError:
            pytest.fail(f"Prediction value '{pred_str}' at row {i+2} is not a valid float.")