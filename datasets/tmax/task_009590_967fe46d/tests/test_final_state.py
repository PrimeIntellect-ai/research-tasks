# test_final_state.py
import os
import pytest

def test_anomalies_parquet_exists_and_correct():
    parquet_path = '/home/user/anomalies.parquet'
    assert os.path.exists(parquet_path), f"Expected output file {parquet_path} does not exist."

    try:
        import pandas as pd
    except ImportError:
        pytest.fail("pandas is not installed, cannot verify parquet file.")

    try:
        df = pd.read_parquet(parquet_path)
    except Exception as e:
        pytest.fail(f"Failed to read {parquet_path} as a Parquet file: {e}")

    expected_columns = {'device', 'hour', 'mean_val', 'rolling_avg'}
    actual_columns = set(df.columns)
    assert expected_columns.issubset(actual_columns), f"Missing columns in output. Expected {expected_columns}, got {actual_columns}"

    assert len(df) == 2, f"Expected exactly 2 anomalies, but found {len(df)}."

    # Check Sensor A anomaly
    a_anom = df[df['device'] == 'sensor_A']
    assert len(a_anom) == 1, "Expected exactly 1 anomaly for sensor_A."
    a_row = a_anom.iloc[0]

    assert abs(a_row['mean_val'] - 34.5) < 0.1, f"Expected sensor_A mean_val around 34.5, got {a_row['mean_val']}"
    assert abs(a_row['rolling_avg'] - 25.833) < 0.1, f"Expected sensor_A rolling_avg around 25.83, got {a_row['rolling_avg']}"

    # Check Sensor B anomaly
    b_anom = df[df['device'] == 'sensor_B']
    assert len(b_anom) == 1, "Expected exactly 1 anomaly for sensor_B."
    b_row = b_anom.iloc[0]

    assert abs(b_row['mean_val'] - 5.0) < 0.1, f"Expected sensor_B mean_val around 5.0, got {b_row['mean_val']}"
    assert abs(b_row['rolling_avg'] - 12.333) < 0.1, f"Expected sensor_B rolling_avg around 12.33, got {b_row['rolling_avg']}"