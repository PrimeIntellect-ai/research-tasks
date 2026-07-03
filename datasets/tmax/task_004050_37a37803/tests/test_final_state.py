# test_final_state.py
import os
import csv
from collections import defaultdict

def test_c_source_exists():
    assert os.path.isfile("/home/user/process_sensors.c"), "C source file /home/user/process_sensors.c is missing."

def test_summary_csv_exists():
    assert os.path.isfile("/home/user/summary.csv"), "Output file /home/user/summary.csv is missing."

def test_summary_csv_contents():
    input_path = "/home/user/sensors.csv"
    output_path = "/home/user/summary.csv"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    # Compute expected results dynamically
    sensor_temps = defaultdict(list)
    with open(input_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 4:
                continue

            timestamp, sensor_id_str, temp_str, err_str = row[0], row[1], row[2], row[3]
            sensor_id = int(sensor_id_str)
            temp = float(temp_str)

            # Handle missing error code
            if err_str.strip() == "":
                err_code = -1
            else:
                err_code = int(err_str)

            # Outlier rejection
            if temp < -50.0 or temp > 150.0:
                continue

            # Filtering valid readings
            if err_code not in (0, -1):
                continue

            sensor_temps[sensor_id].append(temp)

    expected_output = [["sensor_id", "avg_temperature"]]
    for sid in sorted(sensor_temps.keys()):
        temps = sensor_temps[sid]
        avg_temp = sum(temps) / len(temps)
        expected_output.append([str(sid), f"{avg_temp:.2f}"])

    # Read actual output
    with open(output_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_output = list(reader)

    assert len(actual_output) > 0, "Output CSV is empty."
    assert actual_output[0] == ["sensor_id", "avg_temperature"], f"Incorrect header in summary.csv: {actual_output[0]}"

    assert len(actual_output) == len(expected_output), f"Expected {len(expected_output)} rows in summary.csv, got {len(actual_output)}"

    for i, (expected, actual) in enumerate(zip(expected_output, actual_output)):
        assert expected == actual, f"Row {i} mismatch. Expected {expected}, got {actual}"