# test_final_state.py

import os
import pandas as pd
from sklearn.metrics import mean_squared_error

def test_scored_pipeline_output():
    output_path = "/home/user/scored_pipeline_output.csv"
    input_path = "/app/data/batch_001.csv"

    assert os.path.isfile(output_path), f"Expected output file {output_path} is missing."
    assert os.path.isfile(input_path), f"Expected input file {input_path} is missing."

    # Load truth data
    df_true = pd.read_csv(input_path)
    # Compute the ground truth score based on the hidden equation
    df_true['score'] = 3.14 * df_true['feature_A'] - 1.618 * df_true['feature_B'] + 2.718 * df_true['feature_C'] + 42.0
    df_true = df_true[['id', 'score']].sort_values('id').reset_index(drop=True)

    # Load agent prediction
    try:
        df_pred = pd.read_csv(output_path)
    except Exception as e:
        assert False, f"Failed to read {output_path} as CSV: {e}"

    assert 'id' in df_pred.columns and 'score' in df_pred.columns, "Output CSV must contain exactly 'id' and 'score' columns."
    assert len(df_pred.columns) == 2, f"Output CSV must contain exactly two columns, found {len(df_pred.columns)}."

    df_pred = df_pred.sort_values('id').reset_index(drop=True)

    assert len(df_true) == len(df_pred), f"Row count mismatch. Expected {len(df_true)}, got {len(df_pred)}."

    # Calculate MSE
    mse = mean_squared_error(df_true['score'], df_pred['score'])

    threshold = 0.0001
    assert mse <= threshold, f"MSE threshold failed. Expected MSE <= {threshold}, got {mse}"