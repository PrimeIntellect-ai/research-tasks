# test_final_state.py

import os
import json
import pandas as pd
from sklearn.metrics import mean_squared_error
import pytest

def test_predictions_csv_and_mse():
    """Verify that predictions.csv exists, has the correct format, and MSE <= 5.0."""
    csv_path = '/home/user/predictions.csv'
    assert os.path.exists(csv_path), f"File not found: {csv_path}"

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path} as CSV: {e}")

    assert 'true_index' in df.columns, "Column 'true_index' missing from predictions.csv"
    assert 'predicted_index' in df.columns, "Column 'predicted_index' missing from predictions.csv"

    # Check MSE
    try:
        mse = mean_squared_error(df['true_index'], df['predicted_index'])
    except Exception as e:
        pytest.fail(f"Failed to compute MSE: {e}")

    assert mse <= 5.0, f"MSE is {mse}, which is greater than the threshold of 5.0"

def test_model_artifacts_json():
    """Verify that model_artifacts.json exists and is valid JSON."""
    json_path = '/home/user/model_artifacts.json'
    assert os.path.exists(json_path), f"File not found: {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {json_path} as JSON: {e}")

    assert isinstance(data, dict), f"Expected JSON object in {json_path}"

def test_cpp_pipeline_exists():
    """Verify that pipeline.cpp exists."""
    cpp_path = '/home/user/pipeline.cpp'
    assert os.path.exists(cpp_path), f"File not found: {cpp_path}"