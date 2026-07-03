# test_final_state.py
import os
import pandas as pd
import numpy as np

def test_rolling_metrics_mse():
    pred_path = "/home/user/rolling_metrics.csv"
    true_path = "/app/ground_truth_metrics.csv"

    assert os.path.exists(pred_path), f"Output file is missing: {pred_path}"
    assert os.path.exists(true_path), f"Ground truth file is missing: {true_path}"

    try:
        pred_df = pd.read_csv(pred_path)
    except Exception as e:
        assert False, f"Failed to read {pred_path} as CSV: {e}"

    try:
        true_df = pd.read_csv(true_path)
    except Exception as e:
        assert False, f"Failed to read {true_path} as CSV: {e}"

    assert 'second' in pred_df.columns, "Output CSV is missing the 'second' column"
    assert 'rolling_size' in pred_df.columns, "Output CSV is missing the 'rolling_size' column"

    # Ensure the dataframe is sorted by second to align with ground truth
    pred_df = pred_df.sort_values('second').reset_index(drop=True)
    true_df = true_df.sort_values('second').reset_index(drop=True)

    assert len(pred_df) == len(true_df), f"Expected {len(true_df)} rows, but got {len(pred_df)} rows."

    # Check if the 'second' column matches exactly
    np.testing.assert_array_equal(
        pred_df['second'].values, 
        true_df['second'].values, 
        err_msg="The 'second' column does not match the expected values (0 to 59)."
    )

    # Compute MSE
    mse = np.mean((pred_df['rolling_size'] - true_df['rolling_size'])**2)

    threshold = 0.1
    assert mse <= threshold, f"MSE is {mse}, which is greater than the threshold of {threshold}. The 'rolling_size' values are incorrect."