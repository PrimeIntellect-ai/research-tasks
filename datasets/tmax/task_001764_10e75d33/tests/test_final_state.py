# test_final_state.py

import os
import csv

def test_c_source_exists():
    """Test that the C source code file exists."""
    assert os.path.exists("/home/user/process_data.c"), "The C program source file /home/user/process_data.c is missing."

def test_executable_exists():
    """Test that the compiled executable exists."""
    assert os.path.exists("/home/user/processor"), "The compiled executable /home/user/processor is missing. Did you compile the program?"
    assert os.access("/home/user/processor", os.X_OK), "The file /home/user/processor is not executable."

def test_output_file_exists():
    """Test that the output CSV file exists."""
    assert os.path.exists("/home/user/clean_telemetry.csv"), "The output file /home/user/clean_telemetry.csv is missing. Did you run the program?"

def test_output_content_correct():
    """Test that the output CSV content matches the expected reshaped and deduplicated data."""
    input_file = "/home/user/raw_sensors.csv"
    output_file = "/home/user/clean_telemetry.csv"

    assert os.path.exists(input_file), f"Input file {input_file} is missing."
    assert os.path.exists(output_file), f"Output file {output_file} is missing."

    # Derive expected output
    expected_rows = []
    seen = set()

    with open(input_file, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 5:
                continue
            sensor_id = row[0]
            timestamp = row[1]
            metric_A = float(row[2])
            metric_B = float(row[3])
            event_log = row[4]

            key = (sensor_id, timestamp)
            if key in seen:
                continue
            seen.add(key)

            # Normalize event log
            event = event_log.split(';')[0].lower()

            expected_rows.append(f"{sensor_id},{timestamp},metric_A,{metric_A:.2f},{event}")
            expected_rows.append(f"{sensor_id},{timestamp},metric_B,{metric_B:.2f},{event}")

    expected_content = "\n".join(expected_rows)

    with open(output_file, "r") as f:
        actual_content = f.read().strip()

    # We compare line by line to give better error messages
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in output, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Row {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"