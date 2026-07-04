# test_final_state.py
import os
import pandas as pd
import numpy as np

def test_output_csv_exists():
    path = "/home/user/analyzer/output.csv"
    assert os.path.isfile(path), f"Expected output file {path} to exist. Did you run the compiled analyzer?"

def test_mae_threshold():
    agent_csv = "/home/user/analyzer/output.csv"
    truth_csv = "/app/expected_truth.csv"

    assert os.path.isfile(agent_csv), f"Agent output {agent_csv} is missing."
    assert os.path.isfile(truth_csv), f"Truth file {truth_csv} is missing."

    try:
        df_agent = pd.read_csv(agent_csv, names=['frame', 'intensity'])
        # Force numeric types to avoid issues with garbled lines
        df_agent['frame'] = pd.to_numeric(df_agent['frame'], errors='coerce')
        df_agent['intensity'] = pd.to_numeric(df_agent['intensity'], errors='coerce')

        # Drop any rows that couldn't be parsed as numbers (garbled output)
        if df_agent.isnull().values.any():
            assert False, "Output CSV contains garbled lines or non-numeric data."

        df_agent = df_agent.sort_values('frame').reset_index(drop=True)
    except Exception as e:
        assert False, f"Failed to read or parse agent CSV: {e}"

    try:
        df_truth = pd.read_csv(truth_csv, names=['frame', 'intensity'])
        df_truth = df_truth.sort_values('frame').reset_index(drop=True)
    except Exception as e:
        assert False, f"Failed to read truth CSV: {e}"

    assert len(df_agent) == 300, f"Expected exactly 300 frames in output, found {len(df_agent)}."
    assert df_agent['frame'].nunique() == 300, "Frames are not unique in the output. A race condition may still exist."

    # Calculate Mean Absolute Error
    mae = np.mean(np.abs(df_agent['intensity'] - df_truth['intensity']))

    assert mae <= 1.5, f"Mean Absolute Error (MAE) is {mae:.4f}, which is above the threshold of 1.5. Synchronization issues might still be causing incorrect intensity calculations."