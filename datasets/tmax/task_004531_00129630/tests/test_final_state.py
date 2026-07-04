# test_final_state.py
import os
import csv
import math
import pytest

def test_validated_configs_exists_and_utf8():
    file_path = '/home/user/validated_configs.csv'
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
    except UnicodeDecodeError:
        pytest.fail(f"File {file_path} is not encoded in UTF-8.")

def test_validated_configs_content():
    file_path = '/home/user/validated_configs.csv'
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    expected_data = [
        ('2023-10-03', 'AuthService', 'MemoryLimit', 2048, 1365.33),
        ('2023-10-04', 'AuthService', 'MemoryLimit', 4096, 2389.33),
        ('2023-10-05', 'AuthService', 'MemoryLimit', 8192, 4778.67),
        ('2023-10-03', 'AuthService', 'Timeout', 300, 200.0),
        ('2023-10-04', 'AuthService', 'Timeout', 1500, 666.67),
        ('2023-10-03', 'PaymentService', 'Timeout', 500, 500.0),
        ('2023-10-04', 'PaymentService', 'Timeout', 500, 500.0),
        ('2023-10-05', 'PaymentService', 'Timeout', 500, 500.0),
        ('2023-10-06', 'PaymentService', 'Timeout', 500, 500.0),
    ]

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("The CSV file is empty.")

        expected_header = ['Date', 'Service', 'Parameter', 'Value', 'RollingAvg']
        assert header == expected_header, f"Expected header {expected_header}, got {header}"

        actual_rows = list(reader)
        assert len(actual_rows) == len(expected_data), f"Expected {len(expected_data)} rows, got {len(actual_rows)} rows."

        for i, (actual, expected) in enumerate(zip(actual_rows, expected_data)):
            assert len(actual) == 5, f"Row {i+1} does not have exactly 5 columns."

            assert actual[0] == expected[0], f"Row {i+1} Date mismatch: expected {expected[0]}, got {actual[0]}"
            assert actual[1] == expected[1], f"Row {i+1} Service mismatch: expected {expected[1]}, got {actual[1]}"
            assert actual[2] == expected[2], f"Row {i+1} Parameter mismatch: expected {expected[2]}, got {actual[2]}"

            try:
                actual_value = int(actual[3])
            except ValueError:
                pytest.fail(f"Row {i+1} Value '{actual[3]}' is not a valid integer.")
            assert actual_value == expected[3], f"Row {i+1} Value mismatch: expected {expected[3]}, got {actual_value}"

            try:
                actual_rolling = float(actual[4])
            except ValueError:
                pytest.fail(f"Row {i+1} RollingAvg '{actual[4]}' is not a valid float.")

            assert math.isclose(actual_rolling, expected[4], rel_tol=1e-3), \
                f"Row {i+1} RollingAvg mismatch: expected {expected[4]}, got {actual_rolling}"