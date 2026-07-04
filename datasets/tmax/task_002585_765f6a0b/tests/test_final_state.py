# test_final_state.py
import os
import pandas as pd
import numpy as np

def test_smoothed_cpu_output():
    agent_file = '/home/user/smoothed_cpu.csv'
    gt_file = '/app/gt_smoothed.csv'

    # 1. Check if the output file exists
    assert os.path.exists(agent_file), f"Agent output file not found at {agent_file}"
    assert os.path.isfile(agent_file), f"Path {agent_file} is not a file"

    # 2. Load the data
    try:
        df_agent = pd.read_csv(agent_file)
    except Exception as e:
        raise AssertionError(f"Failed to read agent CSV file: {e}")

    try:
        df_gt = pd.read_csv(gt_file)
    except Exception as e:
        raise AssertionError(f"Failed to read ground truth CSV file: {e}")

    # 3. Check for required columns
    assert 'second' in df_agent.columns, "Column 'second' missing in agent CSV"
    assert 'smoothed_cpu' in df_agent.columns, "Column 'smoothed_cpu' missing in agent CSV"

    # 4. Sort and align by 'second'
    df_agent = df_agent.sort_values('second').reset_index(drop=True)
    df_gt = df_gt.sort_values('second').reset_index(drop=True)

    # 5. Truncate to the shortest length and check minimum length
    min_len = min(len(df_agent), len(df_gt))
    assert min_len >= 50, f"Too many missing frames. Found {min_len}/60. Expected at least 50."

    # 6. Compute MSE
    agent_values = df_agent['smoothed_cpu'][:min_len].values
    gt_values = df_gt['smoothed_cpu_gt'][:min_len].values

    mse = np.mean((agent_values - gt_values)**2)

    # 7. Assert MSE is within threshold
    threshold = 2.0
    assert mse <= threshold, f"MSE is {mse:.4f}, which is greater than the threshold of {threshold}. The OCR parsing or rolling average calculation might be inaccurate."