# test_final_state.py

import os
import re
import stat
import pandas as pd
import numpy as np
import pytest

def test_rolling_averages_csv():
    """Verify that the rolling averages CSV exists, has correct headers, and meets the MSE threshold."""
    csv_path = '/home/user/rolling_averages.csv'
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"Path {csv_path} is not a file."

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path} as CSV: {e}")

    expected_headers = ['Index', 'Value', 'RollingAvg']
    assert list(df.columns) == expected_headers, f"CSV headers {list(df.columns)} do not match expected {expected_headers}."

    truth = np.array([45.0, 48.5, 48.33, 53.33, 54.33, 55.0, 55.67, 59.0, 65.67, 67.67])

    try:
        agent_vals = df['RollingAvg'].astype(float).values
    except ValueError:
        pytest.fail("RollingAvg column contains non-numeric values.")

    min_len = min(len(truth), len(agent_vals))
    mse = np.mean((truth[:min_len] - agent_vals[:min_len])**2) if min_len > 0 else 100.0

    if len(truth) != len(agent_vals):
        mse += abs(len(truth) - len(agent_vals)) * 10.0

    threshold = 2.0
    assert mse <= threshold, f"MSE of RollingAvg is {mse:.4f}, which exceeds the threshold of {threshold}."

def test_process_metrics_script():
    """Verify that the script /home/user/process_metrics.sh exists and is executable."""
    script_path = '/home/user/process_metrics.sh'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"Script {script_path} is not executable."

def test_cron_schedule_file():
    """Verify that the cron file /home/user/metrics_pipeline.cron exists and contains the correct schedule."""
    cron_path = '/home/user/metrics_pipeline.cron'
    assert os.path.exists(cron_path), f"Cron file {cron_path} does not exist."
    assert os.path.isfile(cron_path), f"Path {cron_path} is not a file."

    with open(cron_path, 'r') as f:
        content = f.read().strip()

    # Look for a cron expression that runs every 15 minutes and executes the script
    # E.g., '*/15 * * * * /home/user/process_metrics.sh'
    # Also allow '0,15,30,45 * * * * ...'
    assert '/home/user/process_metrics.sh' in content, f"Cron file does not reference /home/user/process_metrics.sh"

    # Check for 15-minute intervals
    valid_cron_start = re.search(r'^(\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*', content, re.MULTILINE)
    assert valid_cron_start is not None, f"Cron file does not contain a valid 15-minute schedule (e.g. '*/15 * * * *'). Content: {content}"