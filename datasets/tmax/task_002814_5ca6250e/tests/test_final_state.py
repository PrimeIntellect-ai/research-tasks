# test_final_state.py

import os
import pytest
import pandas as pd
import numpy as np

def test_processed_features_exists():
    path = "/home/user/processed_features.parquet"
    assert os.path.exists(path), f"Missing required file: {path}"
    assert os.path.isfile(path), f"Expected a file, but found a directory: {path}"

def test_processed_features_columns():
    path = "/home/user/processed_features.parquet"
    assert os.path.exists(path), "Parquet file not found."

    df_agent = pd.read_parquet(path)
    expected_columns = {'id', 'cleaned_sensor_val', 'feature_score'}
    actual_columns = set(df_agent.columns)

    assert actual_columns == expected_columns, (
        f"Columns in parquet file do not match expected. "
        f"Expected: {expected_columns}, Actual: {actual_columns}"
    )

def test_feature_score_mae():
    agent_path = "/home/user/processed_features.parquet"
    raw_path = "/home/user/data/telemetry.csv"

    assert os.path.exists(agent_path), "Agent output parquet file not found."
    assert os.path.exists(raw_path), "Original telemetry CSV file not found."

    df_agent = pd.read_parquet(agent_path)
    df_raw = pd.read_csv(raw_path)

    # Compute true expected values
    med = df_raw['sensor_val'].median()
    df_raw['cleaned'] = df_raw['sensor_val'].fillna(med)

    p01 = df_raw['cleaned'].quantile(0.01)
    p99 = df_raw['cleaned'].quantile(0.99)
    df_raw['cleaned'] = df_raw['cleaned'].clip(lower=p01, upper=p99)

    def compute_true_score(row):
        text = str(row['log_message'])
        words = text.split()
        metric = sum(len(w)**2 for w in words)
        return row['cleaned'] * metric

    df_raw['true_score'] = df_raw.apply(compute_true_score, axis=1)

    # Align and compute MAE
    df_merged = pd.merge(df_raw, df_agent, on='id', how='inner')

    assert len(df_merged) == len(df_raw), "Agent output does not contain all rows from the original dataset."

    mae = np.mean(np.abs(df_merged['true_score'] - df_merged['feature_score']))

    threshold = 0.01
    assert mae < threshold, (
        f"Mean Absolute Error (MAE) of feature_score is too high. "
        f"Expected < {threshold}, but got {mae:.6f}."
    )