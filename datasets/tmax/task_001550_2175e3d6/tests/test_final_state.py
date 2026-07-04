# test_final_state.py
import os
import math

def test_output_files_exist():
    """Verify that the expected output files exist."""
    assert os.path.isfile("/home/user/processed_features.csv"), "/home/user/processed_features.csv is missing."
    assert os.path.isfile("/home/user/invalid_rows.log"), "/home/user/invalid_rows.log is missing."

def test_processed_features_content():
    """Verify the content of processed_features.csv matches the expected logic."""
    if not os.path.isfile("/home/user/raw_sensors.csv"):
        return

    expected_processed = []
    expected_invalid = []

    with open("/home/user/raw_sensors.csv", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 32:
                expected_invalid.append(line)
                continue

            sensor_id_str = parts[0]
            try:
                int(sensor_id_str)
            except ValueError:
                expected_invalid.append(line)
                continue

            timestamp = parts[1]

            try:
                readings = [float(x) for x in parts[2:]]
            except ValueError:
                expected_invalid.append(line)
                continue

            dim1 = sum(readings[0:10]) / 10.0
            dim2 = max(readings[10:20])
            dim3 = min(readings[20:30])

            if math.isnan(dim1) or math.isnan(dim2) or math.isnan(dim3) or \
               math.isinf(dim1) or math.isinf(dim2) or math.isinf(dim3):
                expected_invalid.append(line)
                continue

            dim1 = max(-100.0, min(100.0, dim1))
            dim2 = max(-100.0, min(100.0, dim2))
            dim3 = max(-100.0, min(100.0, dim3))

            expected_processed.append(f"{sensor_id_str},{timestamp},{dim1:.4f},{dim2:.4f},{dim3:.4f}")

    with open("/home/user/processed_features.csv", "r") as f:
        actual_processed = [line.strip() for line in f if line.strip()]

    assert actual_processed == expected_processed, (
        f"processed_features.csv content is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_processed)}\n"
        f"Actual:\n{chr(10).join(actual_processed)}"
    )

def test_invalid_rows_content():
    """Verify the content of invalid_rows.log matches the expected logic."""
    if not os.path.isfile("/home/user/raw_sensors.csv"):
        return

    expected_invalid = []

    with open("/home/user/raw_sensors.csv", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 32:
                expected_invalid.append(line)
                continue

            sensor_id_str = parts[0]
            try:
                int(sensor_id_str)
            except ValueError:
                expected_invalid.append(line)
                continue

            try:
                readings = [float(x) for x in parts[2:]]
            except ValueError:
                expected_invalid.append(line)
                continue

            dim1 = sum(readings[0:10]) / 10.0
            dim2 = max(readings[10:20])
            dim3 = min(readings[20:30])

            if math.isnan(dim1) or math.isnan(dim2) or math.isnan(dim3) or \
               math.isinf(dim1) or math.isinf(dim2) or math.isinf(dim3):
                expected_invalid.append(line)
                continue

    with open("/home/user/invalid_rows.log", "r") as f:
        actual_invalid = [line.strip() for line in f if line.strip()]

    assert actual_invalid == expected_invalid, (
        f"invalid_rows.log content is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_invalid)}\n"
        f"Actual:\n{chr(10).join(actual_invalid)}"
    )