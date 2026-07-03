# test_final_state.py

import os
import json
import csv
import pytest

def test_etl_pipeline_exists_and_multiprocessing():
    """Check if the ETL pipeline script exists and uses multiprocessing."""
    script_path = "/home/user/etl_pipeline.py"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    assert "multiprocessing" in content or "concurrent.futures" in content, \
        "The script does not appear to use the multiprocessing module."

def test_aggregated_json_output():
    """Check if aggregated.json exists and contains the correct aggregated data."""
    output_path = "/home/user/etl_output/aggregated.json"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    assert isinstance(data, list), "Aggregated JSON should be a list of objects."

    expected_data = [
        {"sensor_id": "S1", "metric_type": "temp", "avg_value": 22.0},
        {"sensor_id": "S2", "metric_type": "humidity", "avg_value": 50.0},
        {"sensor_id": "S3", "metric_type": "pressure", "avg_value": 1014.0}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(data)}."

    # Check sorting and exact values
    for i, expected in enumerate(expected_data):
        actual = data[i]
        assert actual.get("sensor_id") == expected["sensor_id"], f"Item {i} sensor_id mismatch."
        assert actual.get("metric_type") == expected["metric_type"], f"Item {i} metric_type mismatch."
        assert abs(actual.get("avg_value", 0) - expected["avg_value"]) < 0.01, f"Item {i} avg_value mismatch."

def test_rejected_records_csv_output():
    """Check if rejected_records.csv exists and contains the correct rejected rows."""
    output_path = "/home/user/etl_output/rejected_records.csv"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    with open(output_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Rejected records CSV is empty."

    header = rows[0]
    expected_header = ["timestamp", "sensor_id", "metric_type", "value", "unit"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    actual_data_rows = sorted([",".join(row) for row in rows[1:]])

    expected_data_rows = sorted([
        "2023-10-01T12:00:00Z,S1,temp,150.0,F",
        "2023-10-01T12:00:00Z,S2,humidity,110.0,%",
        "2023-10-01T13:00:00Z,S4,temp,invalid,C"
    ])

    assert actual_data_rows == expected_data_rows, "Rejected records data mismatch."