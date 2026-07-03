# test_final_state.py
import os
import pandas as pd
import json
import re
import numpy as np

def test_processed_data_mse():
    csv_path = "/app/processed_data.csv"
    assert os.path.exists(csv_path), f"Processed data CSV not found at {csv_path}"

    # Ground truth derivation
    data = []
    with open("/app/data/raw_sensors.jsonl", "r") as f:
        for line in f:
            # Clean up broken unicode escapes
            clean_line = re.sub(r'\\u[0-9a-fA-F]{0,3}[^0-9a-fA-F"]?', '', line)
            try:
                row = json.loads(clean_line)
                data.append(row)
            except:
                pass

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['minute_timestamp'] = df['timestamp'].dt.floor('min')

    long_df = df.melt(id_vars=['minute_timestamp', 'timestamp'], value_vars=['s1', 's2', 's3'], var_name='sensor_id', value_name='raw_value')
    long_df = long_df.dropna(subset=['raw_value'])

    # Calibration formula from image: y = 3.5 * x + -1.2
    long_df['calibrated_mean'] = 3.5 * pd.to_numeric(long_df['raw_value']) - 1.2

    gt_agg = long_df.groupby(['minute_timestamp', 'sensor_id'])['calibrated_mean'].mean().reset_index()
    gt_agg['minute_timestamp'] = gt_agg['minute_timestamp'].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    gt_agg['calibrated_mean'] = gt_agg['calibrated_mean'].round(3)

    # Read agent data
    try:
        agent_df = pd.read_csv(csv_path)
    except Exception as e:
        assert False, f"Failed to read {csv_path}: {e}"

    assert 'minute_timestamp' in agent_df.columns, "Missing 'minute_timestamp' column in processed_data.csv"
    assert 'sensor_id' in agent_df.columns, "Missing 'sensor_id' column in processed_data.csv"
    assert 'calibrated_mean' in agent_df.columns, "Missing 'calibrated_mean' column in processed_data.csv"

    merged = pd.merge(gt_agg, agent_df, on=['minute_timestamp', 'sensor_id'], suffixes=('_gt', '_agent'))

    assert len(merged) > 0, "No matching rows found between ground truth and agent output."
    assert len(merged) >= len(gt_agg) * 0.9, "Agent output is missing a significant number of expected rows."

    mse = np.mean((merged['calibrated_mean_gt'] - merged['calibrated_mean_agent'])**2)

    assert mse <= 0.01, f"MSE is {mse:.5f}, which is greater than the threshold of 0.01"