# test_final_state.py

import os
import re
import math
import pytest

def test_processed_sensors_csv_exists():
    """Verify that the processed CSV file exists."""
    output_path = "/home/user/processed_sensors.csv"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

def test_processed_sensors_csv_content():
    """Verify that the processed CSV file contains the correctly computed and formatted values."""
    raw_log_path = "/home/user/raw_sensors.log"
    assert os.path.isfile(raw_log_path), f"The input file {raw_log_path} is missing."

    expected_lines = []
    with open(raw_log_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue

            # Extract all numbers (integers or floats, positive or negative)
            matches = re.findall(r'-?\d+\.\d+|-?\d+', line)

            # The spatial coordinates (x, y, z) are the last 3 numbers in each log line
            if len(matches) < 3:
                continue

            x, y, z = map(float, matches[-3:])

            # Calculate L2 norm
            norm = math.sqrt(x*x + y*y + z*z)

            # Normalize vector
            if norm == 0:
                nx, ny, nz = 0.0, 0.0, 0.0
            else:
                nx = x / norm
                ny = y / norm
                nz = z / norm

            # Calculate Euclidean distance to reference vector (1.0, 0.0, 0.0)
            dx = nx - 1.0
            dy = ny - 0.0
            dz = nz - 0.0
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)

            # Format to exactly 4 decimal places
            expected_line = f"{x:.4f},{y:.4f},{z:.4f},{nx:.4f},{ny:.4f},{nz:.4f},{dist:.4f}"
            expected_lines.append(expected_line)

    processed_csv_path = "/home/user/processed_sensors.csv"
    with open(processed_csv_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} rows in the output CSV, but found {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Row {i+1} does not match the expected output.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )