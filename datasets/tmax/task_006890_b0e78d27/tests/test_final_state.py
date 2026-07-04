# test_final_state.py

import os
import csv
import json

def test_clean_telemetry_file_exists():
    """Test that the clean_telemetry.csv file was created."""
    file_path = "/home/user/clean_telemetry.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

def test_pipeline_log_file_exists():
    """Test that the pipeline_log.json file was created."""
    file_path = "/home/user/pipeline_log.json"
    assert os.path.isfile(file_path), f"Log file {file_path} does not exist."

def test_clean_telemetry_content():
    """Test that the clean_telemetry.csv has the correct data and formatting."""
    file_path = "/home/user/clean_telemetry.csv"

    expected_rows = [
        ['2023-10-01T10:00:00', '20.00', '1013.25', '0.00'],
        ['2023-10-01T10:01:00', '22.00', '1012.25', '2.00'],
        ['2023-10-01T10:02:00', '26.00', '1011.00', '4.00'],
        ['2023-10-01T10:03:00', '32.00', '1009.50', '6.00'],
        ['2023-10-01T10:04:00', '40.00', '1007.50', '8.00'],
        ['2023-10-01T10:05:00', '50.00', '1005.00', '10.00'],
        ['2023-10-01T10:06:00', '62.00', '1002.25', '12.00']
    ]

    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["timestamp", "temperature", "pressure", "temp_roc"], \
            f"Incorrect header in {file_path}: {header}"

        rows = list(reader)
        assert len(rows) == 7, f"Expected 7 data rows in {file_path}, found {len(rows)}"

        for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
            # Check timestamp
            assert actual[0] == expected[0], f"Row {i} timestamp mismatch: expected {expected[0]}, got {actual[0]}"
            # Check float values (allow slight variations in formatting like '20.0' vs '20.00' if parsed as float, but strict requirement says exactly 2 decimal places)
            try:
                temp = float(actual[1])
                pres = float(actual[2])
                roc = float(actual[3])
            except ValueError:
                assert False, f"Row {i} contains non-numeric values for temperature, pressure, or temp_roc."

            assert f"{temp:.2f}" == expected[1], f"Row {i} temperature mismatch: expected {expected[1]}, got {actual[1]}"
            assert f"{pres:.2f}" == expected[2], f"Row {i} pressure mismatch: expected {expected[2]}, got {actual[2]}"
            assert f"{roc:.2f}" == expected[3], f"Row {i} temp_roc mismatch: expected {expected[3]}, got {actual[3]}"

def test_pipeline_log_content():
    """Test that the pipeline_log.json contains the correct metrics."""
    file_path = "/home/user/pipeline_log.json"

    with open(file_path, "r") as f:
        try:
            log_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    assert "imputed_temperature_count" in log_data, "Missing 'imputed_temperature_count' in JSON log."
    assert "imputed_pressure_count" in log_data, "Missing 'imputed_pressure_count' in JSON log."
    assert "max_temp_roc" in log_data, "Missing 'max_temp_roc' in JSON log."

    assert log_data["imputed_temperature_count"] == 2, \
        f"Expected imputed_temperature_count to be 2, got {log_data['imputed_temperature_count']}"
    assert log_data["imputed_pressure_count"] == 2, \
        f"Expected imputed_pressure_count to be 2, got {log_data['imputed_pressure_count']}"

    # Check max_temp_roc (float comparison)
    max_roc = log_data["max_temp_roc"]
    assert isinstance(max_roc, (int, float)), "max_temp_roc should be a number."
    assert abs(max_roc - 12.0) < 1e-5, f"Expected max_temp_roc to be 12.0, got {max_roc}"