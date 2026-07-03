# test_final_state.py

import os
import pytest
import re

try:
    import pandas as pd
except ImportError:
    pd = None

PARQUET_PATH = '/home/user/output/clean_data.parquet'
REPORT_PATH = '/home/user/output/report.md'

@pytest.mark.skipif(pd is None, reason="pandas is required to read parquet files")
def test_parquet_file_exists_and_valid():
    assert os.path.exists(PARQUET_PATH), f"Output Parquet file not found at {PARQUET_PATH}"

    try:
        df = pd.read_parquet(PARQUET_PATH)
    except Exception as e:
        pytest.fail(f"Failed to read Parquet file: {e}")

    expected_columns = {'timestamp', 'sensor_id', 'temperature', 'humidity'}
    assert expected_columns.issubset(set(df.columns)), f"Parquet file missing expected columns. Found: {df.columns}"

    # Assert constraints
    assert df['temperature'].min() >= -50.0, "Found temperature below -50.0 in final data"
    assert df['temperature'].max() <= 150.0, "Found temperature above 150.0 in final data"
    assert df['humidity'].min() >= 0.0, "Found humidity below 0.0 in final data"
    assert df['humidity'].max() <= 100.0, "Found humidity above 100.0 in final data"
    assert not df.isnull().any().any(), "Found null/NaN values in final data"

    # Check that timestamps are at 5-minute intervals
    # Since timestamp might be a string or datetime, convert to datetime
    timestamps = pd.to_datetime(df['timestamp'])
    minutes = timestamps.dt.minute
    assert all(minutes % 5 == 0), "Not all timestamps are at strictly 5-minute intervals"

@pytest.mark.skipif(pd is None, reason="pandas is required to read parquet files")
def test_report_matches_parquet():
    assert os.path.exists(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

    df = pd.read_parquet(PARQUET_PATH)

    total_sensors = df['sensor_id'].nunique()
    total_records = len(df)

    # Calculate hottest sensor
    avg_temps = df.groupby('sensor_id')['temperature'].mean()
    hottest_sensor = avg_temps.idxmax()
    hottest_temp = avg_temps.max()

    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        report_content = f.read()

    assert f"Total sensors processed: {total_sensors}" in report_content, "Report does not contain correct total sensors"
    assert f"Total valid records after resampling: {total_records}" in report_content, "Report does not contain correct total records"
    assert f"Sensor with highest average temp: {hottest_sensor}" in report_content, "Report does not contain correct hottest sensor"

    # The temperature should be formatted to 2 decimal places
    expected_temp_str = f"{hottest_temp:.2f}"
    assert f"Average temp of hottest sensor: {expected_temp_str}" in report_content, "Report does not contain correct hottest sensor average temperature"