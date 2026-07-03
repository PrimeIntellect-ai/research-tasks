# test_final_state.py
import os
import json
import csv
import math
import pytest

def test_report_json_exists():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), f"The file {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a valid file."

def test_report_json_content():
    csv_path = "/home/user/sensor_data.csv"
    assert os.path.exists(csv_path), f"The original data file {csv_path} is missing."

    valid_temperatures = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Check timestamp
                if not row["timestamp"].strip():
                    continue
                # Check sensor_id
                sensor_id = int(row["sensor_id"])
                if not (1 <= sensor_id <= 10):
                    continue
                # Check temperature
                temperature = float(row["temperature"])
                if not (-50.0 <= temperature <= 50.0):
                    continue
                # Check humidity
                humidity = float(row["humidity"])
                if not (0.0 <= humidity <= 100.0):
                    continue

                valid_temperatures.append(temperature)
            except (ValueError, KeyError, TypeError):
                # Discard rows with missing or unparseable data
                continue

    n = len(valid_temperatures)
    assert n > 0, "No valid rows found in the CSV data."

    # Calculate statistics
    mean_temp = sum(valid_temperatures) / n
    variance = sum((x - mean_temp) ** 2 for x in valid_temperatures) / (n - 1)
    std_dev = math.sqrt(variance)

    margin_of_error = 1.96 * (std_dev / math.sqrt(n))
    ci_lower = mean_temp - margin_of_error
    ci_upper = mean_temp + margin_of_error

    model_validated = (ci_lower <= 21.5 <= ci_upper)

    # Read and validate the generated JSON report
    report_path = "/home/user/report.json"
    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    # Check keys and values
    assert "valid_rows" in report, "Key 'valid_rows' is missing from the JSON report."
    assert report["valid_rows"] == n, f"Expected 'valid_rows' to be {n}, got {report['valid_rows']}."

    assert "mean_temperature" in report, "Key 'mean_temperature' is missing from the JSON report."
    assert math.isclose(report["mean_temperature"], round(mean_temp, 4), abs_tol=0.0002), \
        f"Expected 'mean_temperature' to be approx {round(mean_temp, 4)}, got {report['mean_temperature']}."

    assert "ci_lower" in report, "Key 'ci_lower' is missing from the JSON report."
    assert math.isclose(report["ci_lower"], round(ci_lower, 4), abs_tol=0.0002), \
        f"Expected 'ci_lower' to be approx {round(ci_lower, 4)}, got {report['ci_lower']}."

    assert "ci_upper" in report, "Key 'ci_upper' is missing from the JSON report."
    assert math.isclose(report["ci_upper"], round(ci_upper, 4), abs_tol=0.0002), \
        f"Expected 'ci_upper' to be approx {round(ci_upper, 4)}, got {report['ci_upper']}."

    assert "model_validated" in report, "Key 'model_validated' is missing from the JSON report."
    assert report["model_validated"] is model_validated, \
        f"Expected 'model_validated' to be {model_validated}, got {report['model_validated']}."