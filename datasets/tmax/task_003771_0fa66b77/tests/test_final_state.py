# test_final_state.py

import os
import pandas as pd
from sklearn.metrics import mean_squared_error
import pytest

def test_clean_data_script_exists():
    script_path = "/home/user/clean_data.py"
    assert os.path.isfile(script_path), f"Expected script missing at {script_path}"

def test_processed_data_exists():
    output_path = "/home/user/processed_sensor_data.csv"
    assert os.path.isfile(output_path), f"Expected output data missing at {output_path}"

def test_processed_data_columns():
    output_path = "/home/user/processed_sensor_data.csv"
    df = pd.read_csv(output_path)
    expected_columns = ['timestamp', 'value']
    assert list(df.columns) == expected_columns, f"Expected columns {expected_columns}, but got {list(df.columns)}"

def test_processed_data_mse():
    output_path = "/home/user/processed_sensor_data.csv"
    truth_path = "/ground_truth/expected_sensor_data.csv"

    assert os.path.isfile(output_path), f"Output file missing: {output_path}"
    assert os.path.isfile(truth_path), f"Truth file missing: {truth_path}"

    pred = pd.read_csv(output_path, parse_dates=['timestamp']).set_index('timestamp')
    true = pd.read_csv(truth_path, parse_dates=['timestamp']).set_index('timestamp')

    common_idx = pred.index.intersection(true.index)
    assert len(common_idx) > 0, "No common timestamps found between the predicted and expected data."

    mse = mean_squared_error(true.loc[common_idx, 'value'], pred.loc[common_idx, 'value'])

    threshold = 0.01
    assert mse <= threshold, f"MSE is {mse}, which is greater than the threshold of {threshold}"