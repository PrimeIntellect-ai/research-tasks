# test_final_state.py

import os
import re
import pytest
import struct

def parse_raw_sensors(filepath):
    """Parses the raw sensors file and returns a list of lists of floats."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Example line: [INFO] MSG_ID=101 : F1=0.123456789 | F2=1.987654321 | F3=3.333333333 | F4=4.444444444
            match = re.search(r'F1=([^\s|]+)\s*\|\s*F2=([^\s|]+)\s*\|\s*F3=([^\s|]+)\s*\|\s*F4=([^\s|]+)', line)
            if match:
                data.append([match.group(1), match.group(2), match.group(3), match.group(4)])
    return data

def test_features_csv():
    features_path = "/home/user/features.csv"
    raw_path = "/home/user/raw_sensors.txt"

    assert os.path.exists(features_path), f"{features_path} does not exist."
    assert os.path.exists(raw_path), f"{raw_path} does not exist."

    expected_data = parse_raw_sensors(raw_path)

    with open(features_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_data), "Number of rows in features.csv does not match raw_sensors.txt."

    for i, (actual_line, expected_row) in enumerate(zip(actual_lines, expected_data)):
        expected_line = ",".join(expected_row)
        assert actual_line == expected_line, f"Row {i+1} in features.csv is incorrect. Expected {expected_line}, got {actual_line}"

def test_projected_double_csv():
    raw_path = "/home/user/raw_sensors.txt"
    double_path = "/home/user/projected_double.csv"

    assert os.path.exists(double_path), f"{double_path} does not exist."

    expected_data = parse_raw_sensors(raw_path)

    with open(double_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_data), "Number of rows in projected_double.csv is incorrect."

    for i, (actual_line, expected_row) in enumerate(zip(actual_lines, expected_data)):
        f1, f2, f3, f4 = map(float, expected_row)
        pc1 = 0.5 * f1 + 0.5 * f2 + 0.5 * f3 + 0.5 * f4
        pc2 = 0.5 * f1 - 0.5 * f2 + 0.5 * f3 - 0.5 * f4

        parts = actual_line.split(',')
        assert len(parts) == 2, f"Row {i+1} in projected_double.csv does not have 2 columns."

        actual_pc1, actual_pc2 = map(float, parts)

        assert abs(actual_pc1 - pc1) < 1e-5, f"Row {i+1} PC1 double mismatch. Expected ~{pc1}, got {actual_pc1}"
        assert abs(actual_pc2 - pc2) < 1e-5, f"Row {i+1} PC2 double mismatch. Expected ~{pc2}, got {actual_pc2}"

def test_max_error_txt():
    float_path = "/home/user/projected_float.csv"
    double_path = "/home/user/projected_double.csv"
    error_path = "/home/user/max_error.txt"

    assert os.path.exists(float_path), f"{float_path} does not exist."
    assert os.path.exists(double_path), f"{double_path} does not exist."
    assert os.path.exists(error_path), f"{error_path} does not exist."

    with open(float_path, 'r') as f:
        float_lines = [line.strip() for line in f if line.strip()]

    with open(double_path, 'r') as f:
        double_lines = [line.strip() for line in f if line.strip()]

    assert len(float_lines) == len(double_lines), "Mismatch in number of rows between float and double CSVs."

    max_diff = 0.0
    for fl_line, db_line in zip(float_lines, double_lines):
        fl_parts = list(map(float, fl_line.split(',')))
        db_parts = list(map(float, db_line.split(',')))

        for fl_val, db_val in zip(fl_parts, db_parts):
            diff = abs(fl_val - db_val)
            if diff > max_diff:
                max_diff = diff

    with open(error_path, 'r') as f:
        reported_error_str = f.read().strip()

    try:
        reported_error = float(reported_error_str)
    except ValueError:
        pytest.fail(f"Could not parse max_error.txt as a float: {reported_error_str}")

    # Check if the reported error matches the actual max difference of their outputs
    assert abs(reported_error - max_diff) < 1e-5, f"max_error.txt mismatch. Expected ~{max_diff:.8f}, got {reported_error:.8f}"

    # Also verify it's formatted to 8 decimal places
    assert re.match(r'^\d+\.\d{8}$', reported_error_str), f"max_error.txt is not formatted to exactly 8 decimal places: {reported_error_str}"