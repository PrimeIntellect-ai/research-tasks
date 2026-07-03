# test_final_state.py
import os
import pandas as pd
from sklearn.metrics import mean_squared_error

def test_recovered_metrics_mse():
    recovered_path = '/home/user/recovered_metrics.csv'
    reference_path = '/app/reference_metrics.csv'

    assert os.path.isfile(recovered_path), f"File not found: {recovered_path}"
    assert os.path.isfile(reference_path), f"Reference file not found: {reference_path}"

    try:
        df_sub = pd.read_csv(recovered_path)
    except Exception as e:
        assert False, f"Failed to read {recovered_path} as CSV: {e}"

    try:
        df_ref = pd.read_csv(reference_path)
    except Exception as e:
        assert False, f"Failed to read {reference_path} as CSV: {e}"

    assert 'value' in df_sub.columns, f"Missing 'value' column in {recovered_path}"
    assert 'value' in df_ref.columns, f"Missing 'value' column in {reference_path}"
    assert 'timestamp' in df_sub.columns, f"Missing 'timestamp' column in {recovered_path}"

    # Ensure lengths match
    assert len(df_sub) == len(df_ref), f"Row count mismatch: expected {len(df_ref)}, got {len(df_sub)}"

    # Sort by timestamp to ensure alignment before comparison
    df_sub_sorted = df_sub.sort_values('timestamp').reset_index(drop=True)
    df_ref_sorted = df_ref.sort_values('timestamp').reset_index(drop=True)

    mse = mean_squared_error(df_ref_sorted['value'], df_sub_sorted['value'])

    assert mse <= 0.0001, f"MSE is too high: {mse} (threshold is <= 0.0001)"