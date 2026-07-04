# test_final_state.py

import os
import csv
import re
import pytest

SCRIPT_PATH = "/home/user/process_sensors.py"
OUTPUT_PATH = "/home/user/cleaned_telemetry.csv"

def test_script_exists():
    """Test that the processing script exists."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."

def test_multiprocessing_used():
    """Test that the script imports/uses multiprocessing or concurrent.futures."""
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    has_multiprocessing = "multiprocessing" in content
    has_concurrent = "ProcessPoolExecutor" in content

    assert has_multiprocessing or has_concurrent, (
        "Script does not appear to use 'multiprocessing' or 'ProcessPoolExecutor' "
        "for parallel data processing as required."
    )

def test_output_exists():
    """Test that the output CSV file was created."""
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing. Did the script run successfully?"

def test_output_content():
    """Test that the output CSV contains the correct headers and correctly processed data."""
    if not os.path.isfile(OUTPUT_PATH):
        pytest.fail(f"Cannot test content because {OUTPUT_PATH} does not exist.")

    with open(OUTPUT_PATH, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Output CSV is empty."

    headers = rows[0]
    expected_headers = ["Sensor_ID", "Log_Time", "Temperature", "Pressure"]
    assert headers == expected_headers, f"Headers {headers} do not match expected {expected_headers}."

    expected_data = [
        ["sensor_1", "1600000000", 20.0, 1000.0],
        ["sensor_1", "1600000010", 21.0, 1005.0],
        ["sensor_1", "1600000020", 21.0, 1010.0],
        ["sensor_1", "1600000040", 23.0, 1020.0],
        ["sensor_2", "1600000010", 15.0, 910.0],
        ["sensor_2", "1600000020", 15.0, 920.0],
        ["sensor_2", "1600000030", 16.0, 930.0],
        ["sensor_2", "1600000040", 17.0, 940.0],
        ["sensor_3", "1600000000", 10.0, 800.0],
        ["sensor_3", "1600000020", 11.0, 810.0],
        ["sensor_3", "1600000030", 12.0, 820.0],
        ["sensor_3", "1600000040", 12.0, 830.0],
        ["sensor_4", "1600000000", 5.0, 700.0],
        ["sensor_4", "1600000010", 5.5, 705.0],
        ["sensor_4", "1600000020", 6.0, 710.0],
        ["sensor_4", "1600000030", 6.0, 715.0],
        ["sensor_4", "1600000040", 7.0, 720.0],
    ]

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_data), (
        f"Expected {len(expected_data)} data rows, but found {len(data_rows)}. "
        "Check your filtering (QC_Flag == PASS) and dropping of leading NaNs."
    )

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert len(actual) == 4, f"Row {i+1} does not have 4 columns."

        actual_sensor = actual[0]
        actual_time = actual[1]

        try:
            actual_temp = float(actual[2])
            actual_pres = float(actual[3])
        except ValueError:
            pytest.fail(f"Row {i+1} contains non-numeric values for Temperature or Pressure: {actual}")

        assert actual_sensor == expected[0], f"Row {i+1}: Expected Sensor_ID '{expected[0]}', got '{actual_sensor}'."
        assert actual_time == expected[1], f"Row {i+1}: Expected Log_Time '{expected[1]}', got '{actual_time}'."

        # Check rounding to 2 decimal places by verifying the string representation
        # and checking the float values are close
        assert format(actual_temp, ".2f") == format(expected[2], ".2f") or str(actual[2]) == str(expected[2]), \
            f"Row {i+1}: Expected Temperature {expected[2]}, got {actual[2]} (check rounding/imputation)."

        assert format(actual_pres, ".2f") == format(expected[3], ".2f") or str(actual[3]) == str(expected[3]), \
            f"Row {i+1}: Expected Pressure {expected[3]}, got {actual[3]} (check rounding/imputation)."