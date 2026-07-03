# test_final_state.py

import os
import csv
import pytest

def test_reshape_c_exists():
    assert os.path.isfile("/home/user/reshape.c"), "The C source file /home/user/reshape.c is missing."

def test_reshape_executable_exists():
    assert os.path.isfile("/home/user/reshape"), "The compiled executable /home/user/reshape is missing."
    assert os.access("/home/user/reshape", os.X_OK), "The file /home/user/reshape is not executable."

def test_workflow_sh_exists():
    assert os.path.isfile("/home/user/workflow.sh"), "The bash script /home/user/workflow.sh is missing."

def test_final_output_exists():
    assert os.path.isfile("/home/user/final_output.csv"), "The final output file /home/user/final_output.csv is missing."

def test_final_output_correctness():
    # Derive expected output from source files
    sensor_data_dir = "/home/user/sensor_data"
    metadata_file = "/home/user/metadata.csv"

    # Read metadata
    metadata = {}
    with open(metadata_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                metadata[row[0].strip()] = row[1].strip()

    # Read and reshape sensor data
    expected_rows = []
    for filename in os.listdir(sensor_data_dir):
        if filename.startswith("floor_") and filename.endswith(".csv"):
            filepath = os.path.join(sensor_data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    continue

                for row in reader:
                    if not row or not "".join(row).strip():
                        continue
                    timestamp = row[0].strip()
                    for i in range(1, len(row)):
                        sensor_id = header[i].strip()
                        value = row[i].strip()
                        sensor_type = metadata.get(sensor_id, "")
                        expected_rows.append((int(timestamp), sensor_id, sensor_type, value))

    # Sort expected: numerically by timestamp (ascending), alphabetically by sensor_id (ascending)
    expected_rows.sort(key=lambda x: (x[0], x[1]))
    expected_lines = [f"{r[0]},{r[1]},{r[2]},{r[3]}" for r in expected_rows]

    # Read actual output
    with open("/home/user/final_output.csv", "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), \
        f"Expected {len(expected_lines)} rows in final_output.csv, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, \
            f"Mismatch at line {i+1} in final_output.csv.\nExpected: {expected}\nGot:      {actual}"