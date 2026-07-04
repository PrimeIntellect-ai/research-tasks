# test_final_state.py

import os
import math
import pytest

def test_workflow_script_exists_and_executable():
    script_path = "/home/user/workflow.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_c_program_exists():
    c_path = "/home/user/process_ts.c"
    assert os.path.exists(c_path), f"{c_path} does not exist."

def test_processed_sensors_output():
    output_path = "/home/user/processed_sensors.csv"
    assert os.path.exists(output_path), f"{output_path} does not exist. Did the workflow run?"

    with open(output_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_data = [
        ("1620000000", "正常启动", 10.0, -0.501634, 0),
        ("1620000060", "警告: 信号弱", 12.0, -0.440830, 0),
        ("1620000120", "Система OK", 14.0, -0.380026, 0),
        ("1620000180", "En attente", 12.0, -0.440830, 0),
        ("1620000240", "ERROR_SPIKE", 100.0, 2.234551, 1),
        ("1620000300", "استئناف", 11.0, -0.471232, 0)
    ]

    assert len(lines) == len(expected_data), f"Expected {len(expected_data)} rows in output, found {len(lines)}."

    for i, (line, expected) in enumerate(zip(lines, expected_data)):
        parts = line.split(",")
        assert len(parts) >= 5, f"Row {i+1} does not have at least 5 comma-separated columns."

        # Reconstruct the event message if it contained commas (none in this dataset, but good practice)
        timestamp = parts[0]
        event_message = ",".join(parts[1:-3])
        interp_val_str = parts[-3]
        zscore_str = parts[-2]
        anomaly_str = parts[-1]

        exp_timestamp, exp_event, exp_interp, exp_zscore, exp_anomaly = expected

        assert timestamp == exp_timestamp, f"Row {i+1} timestamp mismatch: expected {exp_timestamp}, got {timestamp}."
        assert event_message == exp_event, f"Row {i+1} event message mismatch: expected {exp_event}, got {event_message}."

        try:
            interp_val = float(interp_val_str)
            zscore = float(zscore_str)
            anomaly = int(anomaly_str)
        except ValueError:
            pytest.fail(f"Row {i+1} contains non-numeric values for interpolated value, z-score, or anomaly flag.")

        assert math.isclose(interp_val, exp_interp, abs_tol=0.0002), \
            f"Row {i+1} interpolated value mismatch: expected ~{exp_interp:.4f}, got {interp_val_str}."

        assert math.isclose(zscore, exp_zscore, abs_tol=0.0002), \
            f"Row {i+1} Z-score mismatch: expected ~{exp_zscore:.4f}, got {zscore_str}."

        assert anomaly == exp_anomaly, \
            f"Row {i+1} anomaly flag mismatch: expected {exp_anomaly}, got {anomaly}."