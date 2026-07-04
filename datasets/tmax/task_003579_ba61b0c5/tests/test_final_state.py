# test_final_state.py

import os
import subprocess
import pandas as pd
from sklearn.metrics import mean_squared_error
import io

def test_predictions_mse():
    """Test that the predictions exist and the MSE is strictly less than 2.0."""
    preds_path = "/home/user/predictions.csv"
    assert os.path.exists(preds_path), f"Predictions file not found at {preds_path}"

    # Extract ground truth from postgres using psql to avoid psycopg2 dependency
    env = os.environ.copy()
    env['PGPASSWORD'] = 'password123'
    cmd = [
        'psql', '-h', '127.0.0.1', '-U', 'researcher', '-d', 'sensordb',
        '-c', '\\copy (SELECT id, target FROM test_data) TO stdout WITH CSV HEADER'
    ]
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"Failed to extract ground truth from database: {e.stderr}")

    truth_df = pd.read_csv(io.StringIO(result.stdout))
    assert not truth_df.empty, "Ground truth test data is empty."

    try:
        preds_df = pd.read_csv(preds_path)
    except Exception as e:
        raise AssertionError(f"Failed to read predictions CSV: {e}")

    assert 'id' in preds_df.columns, "Predictions CSV must contain an 'id' column."
    assert 'predicted_target' in preds_df.columns, "Predictions CSV must contain a 'predicted_target' column."

    merged = pd.merge(truth_df, preds_df, on="id")
    assert len(merged) == len(truth_df), f"Expected {len(truth_df)} predictions, but matched {len(merged)}."

    mse = mean_squared_error(merged['target'], merged['predicted_target'])

    assert mse <= 2.0, f"FAIL: MSE {mse:.4f} is not <= 2.0"