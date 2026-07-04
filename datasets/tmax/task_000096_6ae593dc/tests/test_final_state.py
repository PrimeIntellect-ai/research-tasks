# test_final_state.py

import os
import pandas as pd
import numpy as np

def test_output_file_exists():
    path = "/home/user/output.csv"
    assert os.path.exists(path), f"The output file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.path.getsize(path) > 0, f"The output file {path} is empty."

def test_output_mae_against_golden():
    golden_path = "/app/golden.csv"
    output_path = "/home/user/output.csv"

    assert os.path.exists(golden_path), f"Golden file {golden_path} missing."
    assert os.path.exists(output_path), f"Output file {output_path} missing."

    col_names = ['timestamp', 'group_id', 'sma']

    try:
        df_golden = pd.read_csv(golden_path, names=col_names)
    except Exception as e:
        assert False, f"Failed to read golden CSV: {e}"

    try:
        df_output = pd.read_csv(output_path, names=col_names)
    except Exception as e:
        assert False, f"Failed to read output CSV: {e}"

    assert len(df_output) == len(df_golden), (
        f"Row count mismatch. Expected {len(df_golden)} rows, but got {len(df_output)} rows. "
        "Check your deduplication logic."
    )

    # Check that timestamp and group_id match exactly
    np.testing.assert_array_equal(
        df_output['timestamp'].values, 
        df_golden['timestamp'].values, 
        err_msg="Timestamps do not match the expected output. Check your deduplication and ordering."
    )

    np.testing.assert_array_equal(
        df_output['group_id'].values, 
        df_golden['group_id'].values, 
        err_msg="Group IDs do not match the expected output. Check your join logic."
    )

    # Calculate MAE of the sma column
    mae = np.max(np.abs(df_output['sma'].values - df_golden['sma'].values))

    threshold = 0.001
    assert mae < threshold, (
        f"Maximum Absolute Error (MAE) for the SMA column is {mae:.6f}, "
        f"which exceeds the threshold of {threshold}. Check your rolling statistics logic."
    )