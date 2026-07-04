# test_final_state.py

import os
import pytest
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def compute_golden_reference():
    # Raw data provided in the setup
    data = [
        (1600000000000, '550e8400-e29b-41d4-a716-446655440000', 72.0, 98.6),
        (1600000001500, '550e8400-e29b-41d4-a716-446655440000', 74.5, 98.7),
        (1600000003000, '550e8400-e29b-41d4-a716-446655440000', 71.0, 98.65),
        (1600000000000, '123e4567-e89b-12d3-a456-426614174000', 80.0, 99.1),
        (1600000002000, '123e4567-e89b-12d3-a456-426614174000', 82.0, 99.3),
        (1600000004500, '123e4567-e89b-12d3-a456-426614174000', 79.0, 99.0),
    ]
    df = pd.DataFrame(data, columns=['timestamp', 'anonymized_id', 'heart_rate', 'temperature'])

    resampled = []
    for uid, group in df.groupby('anonymized_id'):
        group = group.sort_values('timestamp')
        t_min = group['timestamp'].min()
        t_max = group['timestamp'].max()

        # 1000 ms intervals
        t_new = np.arange(t_min, t_max + 1, 1000)
        if t_new[-1] != t_max:
            t_new = np.append(t_new, t_max)

        hr_interp = interp1d(group['timestamp'], group['heart_rate'], kind='linear')(t_new)
        temp_interp = interp1d(group['timestamp'], group['temperature'], kind='linear')(t_new)

        for t, hr, temp in zip(t_new, hr_interp, temp_interp):
            resampled.append((int(t), uid, hr, temp))

    res_df = pd.DataFrame(resampled, columns=['timestamp', 'anonymized_id', 'heart_rate', 'temperature'])

    # Min-Max Normalization across the entire dataset
    hr_min = res_df['heart_rate'].min()
    hr_max = res_df['heart_rate'].max()
    temp_min = res_df['temperature'].min()
    temp_max = res_df['temperature'].max()

    res_df['normalized_hr'] = (res_df['heart_rate'] - hr_min) / (hr_max - hr_min)
    res_df['normalized_temp'] = (res_df['temperature'] - temp_min) / (temp_max - temp_min)

    # Sort output
    res_df = res_df.sort_values(['anonymized_id', 'timestamp']).reset_index(drop=True)
    return res_df[['timestamp', 'anonymized_id', 'normalized_hr', 'normalized_temp']]

def test_processed_data_mse():
    output_path = '/home/user/processed_data.csv'
    assert os.path.exists(output_path), f"Processed data file not found at {output_path}"

    try:
        agent_df = pd.read_csv(output_path)
    except Exception as e:
        pytest.fail(f"Failed to read {output_path} as CSV: {e}")

    expected_columns = ['timestamp', 'anonymized_id', 'normalized_hr', 'normalized_temp']
    for col in expected_columns:
        assert col in agent_df.columns, f"Missing expected column '{col}' in output CSV"

    golden_df = compute_golden_reference()

    # Merge agent and golden dataframes to compare
    merged_df = pd.merge(
        golden_df,
        agent_df,
        on=['timestamp', 'anonymized_id'],
        suffixes=('_golden', '_agent'),
        how='inner'
    )

    # Check if all rows are present
    assert len(merged_df) == len(golden_df), f"Expected {len(golden_df)} rows, but got {len(agent_df)} or missing matches on timestamp/anonymized_id."

    # Compute MSE for normalized_hr
    mse_hr = np.mean((merged_df['normalized_hr_golden'] - merged_df['normalized_hr_agent']) ** 2)

    # Compute MSE for normalized_temp
    mse_temp = np.mean((merged_df['normalized_temp_golden'] - merged_df['normalized_temp_agent']) ** 2)

    # Overall MSE
    overall_mse = (mse_hr + mse_temp) / 2.0

    threshold = 0.001
    assert overall_mse < threshold, f"MSE {overall_mse:.6f} is not strictly less than threshold {threshold}."