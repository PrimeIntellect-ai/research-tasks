# test_final_state.py

import os
import csv
import re
from datetime import datetime, timedelta
import pytest

RAW_DATA_PATH = "/home/user/raw_sensor_logs.csv"
PROCESSED_DATA_PATH = "/home/user/processed_data.csv"

def get_expected_data():
    valid_sensors = {"TempSensor", "Temperatursensor", "温度計"}
    data_by_minute = {}
    min_time = None
    max_time = None

    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["sensor_name"] not in valid_sensors:
                continue

            dt = datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            minute_dt = dt.replace(second=0, microsecond=0)

            if min_time is None or minute_dt < min_time:
                min_time = minute_dt
            if max_time is None or minute_dt > max_time:
                max_time = minute_dt

            reading = float(row["reading"])

            match = re.search(r"\{([^}]+)\}", row["notes"])
            op_code = match.group(1) if match else ""

            if minute_dt not in data_by_minute:
                data_by_minute[minute_dt] = {"readings": [], "op_codes": []}

            data_by_minute[minute_dt]["readings"].append(reading)
            if op_code:
                data_by_minute[minute_dt]["op_codes"].append(op_code)

    expected_rows = []
    if min_time is None:
        return expected_rows

    curr_time = min_time
    last_reading = None

    while curr_time <= max_time:
        ts_str = curr_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        if curr_time in data_by_minute:
            readings = data_by_minute[curr_time]["readings"]
            op_codes = data_by_minute[curr_time]["op_codes"]

            avg_reading = sum(readings) / len(readings)
            # Python's round handles rounding to 2 decimal places
            avg_reading_rounded = f"{round(avg_reading, 2):.2f}"
            last_reading = avg_reading_rounded

            op_code = op_codes[-1] if op_codes else ""

            expected_rows.append([ts_str, "temperature", avg_reading_rounded, op_code])
        else:
            expected_rows.append([ts_str, "temperature", last_reading, "GAP"])

        curr_time += timedelta(minutes=1)

    return expected_rows

def test_processed_file_exists():
    """Test that the processed CSV file was created."""
    assert os.path.exists(PROCESSED_DATA_PATH), f"The file {PROCESSED_DATA_PATH} does not exist."
    assert os.path.isfile(PROCESSED_DATA_PATH), f"The path {PROCESSED_DATA_PATH} is not a file."

def test_processed_file_headers():
    """Test that the processed CSV has the correct headers."""
    with open(PROCESSED_DATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"The file {PROCESSED_DATA_PATH} is empty.")

        expected_headers = ["timestamp", "sensor_name", "reading", "op_code"]
        assert headers == expected_headers, f"Expected headers {expected_headers}, got {headers}."

def test_processed_file_content():
    """Test that the processed CSV content exactly matches the expected resampled data."""
    expected_rows = get_expected_data()

    actual_rows = []
    with open(PROCESSED_DATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), (
        f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}. "
        "Check your start/end times and 1-minute interval logic."
    )

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, (
            f"Row {i+1} mismatch.\nExpected: {expected}\nActual: {actual}\n"
            "Check filtering, mean calculation, gap filling, and op_code extraction."
        )