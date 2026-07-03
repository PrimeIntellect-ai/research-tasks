# test_final_state.py
import os
import pandas as pd
import numpy as np
import pytest

def test_aligned_csv_and_correlation():
    aligned_file = '/home/user/aligned.csv'

    assert os.path.exists(aligned_file), f"Aligned CSV file not found at {aligned_file}."
    assert os.path.isfile(aligned_file), f"Path {aligned_file} is not a file."

    try:
        df = pd.read_csv(aligned_file)
    except Exception as e:
        pytest.fail(f"Failed to read {aligned_file} as CSV: {e}")

    expected_columns = ['timestamp_sec', 'normalized_brightness', 'normalized_sensor']
    for col in expected_columns:
        assert col in df.columns, f"Missing expected column '{col}' in {aligned_file}. Found: {list(df.columns)}"

    assert len(df) > 0, f"The aligned CSV {aligned_file} is empty."

    # Calculate Pearson correlation
    corr = df['normalized_brightness'].corr(df['normalized_sensor'])

    assert not np.isnan(corr), "Pearson correlation is NaN. Check if the normalized columns have zero variance or missing data."

    # The threshold is 0.90
    assert corr >= 0.90, f"Pearson correlation between normalized_brightness and normalized_sensor is {corr:.4f}, which is below the required threshold of 0.90."

def test_cron_job_configuration():
    cron_file = '/home/user/crontab.txt'

    assert os.path.exists(cron_file), f"Cron configuration file not found at {cron_file}."
    assert os.path.isfile(cron_file), f"Path {cron_file} is not a file."

    with open(cron_file, 'r') as f:
        cron_content = f.read().strip()

    assert '15 * * * *' in cron_content, f"Cron expression '15 * * * *' not found in {cron_file}. Content: {cron_content}"
    assert '/home/user/process_latest.sh' in cron_content, f"Command '/home/user/process_latest.sh' not found in {cron_file}. Content: {cron_content}"