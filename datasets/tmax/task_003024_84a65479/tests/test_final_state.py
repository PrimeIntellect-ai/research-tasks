# test_final_state.py

import os
import pytest

def test_summary_csv_exists_and_content():
    """Test that the summary.csv file exists and has the correct output."""
    file_path = '/home/user/data/summary.csv'
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The task requires creating this output file."

    expected_lines = [
        "sensor_id,mean_temp,max_temp,min_temp",
        "S1,14.27,15.00,10.00",
        "S2,20.83,22.00,0.00"
    ]

    with open(file_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {file_path} does not match expected CSV output."

def test_raw_sensors_file_unmodified():
    """Test that the original raw_sensors.jsonl file was not modified."""
    file_path = '/home/user/data/raw_sensors.jsonl'
    assert os.path.isfile(file_path), f"File {file_path} is missing. The original data must not be deleted."

    expected_content = (
        '{"timestamp": "2023-10-01T00:30:00Z", "sensor_id": "S1", "location": "N\\u00f6rth", "temp": 10.0}\n'
        '{"timestamp": "2023-10-01T02:15:00Z", "sensor_id": "S1", "location": "S\\uXXth", "temp": 12.5}\n'
        '{"timestamp": "2023-10-01T05:45:00Z", "sensor_id": "S1", "location": "East", "temp": 15.0}\n'
        '{"timestamp": "2023-10-01T01:15:00Z", "sensor_id": "S2", "location": "W\\u00e9st", "temp": 20.0}\n'
        '{"timestamp": "2023-10-01T04:10:00Z", "sensor_id": "S2", "location": "W\\uYYst", "temp": 22.0}\n'
    )

    with open(file_path, 'r') as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"Content of {file_path} was modified. The task requires leaving it unchanged."