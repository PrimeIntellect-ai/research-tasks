# test_final_state.py
import os
import pandas as pd
import numpy as np

def test_dataset_tsv_exists_and_metric():
    dataset_path = '/home/user/dataset.tsv'
    assert os.path.isfile(dataset_path), f"Output file {dataset_path} does not exist."

    try:
        df_agent = pd.read_csv(dataset_path, sep='\t')
    except Exception as e:
        assert False, f"Failed to read {dataset_path} as TSV: {e}"

    expected_cols = ['segment_id', 'start_ms', 'end_ms', 'duration_ms', 'transcript']
    for c in expected_cols:
        assert c in df_agent.columns, f"Missing expected column '{c}' in {dataset_path}."

    try:
        start_ms = df_agent['start_ms'].astype(float)
        end_ms = df_agent['end_ms'].astype(float)
        actual_duration = df_agent['duration_ms'].astype(float)
    except ValueError as e:
        assert False, f"Numeric columns contain non-numeric data (likely CSV parsing error): {e}"

    expected_duration = end_ms - start_ms
    mae = np.mean(np.abs(expected_duration - actual_duration))

    assert not df_agent['duration_ms'].isna().any(), "duration_ms contains NaN values."
    assert not df_agent['transcript'].isna().any(), "transcript contains NaN values."
    assert len(df_agent) > 0, "The dataset is empty."

    assert mae <= 1.0, f"MAE of duration_ms vs (end_ms - start_ms) is {mae}, which exceeds threshold of 1.0."