# test_final_state.py

import os
import json
import pytest

def test_correlation_file_exists_and_correct():
    metrics_file = "/home/user/metrics/correlation.txt"
    assert os.path.isfile(metrics_file), f"Metrics file {metrics_file} does not exist."

    with open(metrics_file, "r") as f:
        content = f.read().strip()

    assert content == "0.9923", f"Expected correlation to be '0.9923', but got '{content}'."

def test_sensor_1_partition():
    file_path = "/home/user/etl_output/sensor_1/valid.jsonl"
    assert os.path.isfile(file_path), f"Partition file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected 2 lines in {file_path}, got {len(lines)}."

    # Verify JSON structure and content for the first row
    parsed_lines = [json.loads(line) for line in lines]

    # Check keys and types
    for obj in parsed_lines:
        assert "timestamp" in obj and isinstance(obj["timestamp"], str), "Missing or invalid 'timestamp'."
        assert "sensor_id" in obj and isinstance(obj["sensor_id"], int), "Missing or invalid 'sensor_id'."
        assert "temperature" in obj and isinstance(obj["temperature"], float), "Missing or invalid 'temperature'."
        assert "pressure" in obj and isinstance(obj["pressure"], float), "Missing or invalid 'pressure'."
        assert obj["sensor_id"] == 1, "Incorrect sensor_id in partition 1."

    # Check specific values from the truth data
    temperatures = {obj["temperature"] for obj in parsed_lines}
    assert 20.5 in temperatures, "Expected temperature 20.5 not found in sensor 1 partition."
    assert 21.0 in temperatures, "Expected temperature 21.0 not found in sensor 1 partition."

def test_sensor_2_partition():
    file_path = "/home/user/etl_output/sensor_2/valid.jsonl"
    assert os.path.isfile(file_path), f"Partition file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"Expected 1 line in {file_path}, got {len(lines)}."

    obj = json.loads(lines[0])
    assert obj["sensor_id"] == 2, "Incorrect sensor_id in partition 2."
    assert obj["temperature"] == 22.1, "Expected temperature 22.1 not found in sensor 2 partition."
    assert obj["pressure"] == 101.5, "Expected pressure 101.5 not found in sensor 2 partition."

def test_sensor_3_partition():
    file_path = "/home/user/etl_output/sensor_3/valid.jsonl"
    assert os.path.isfile(file_path), f"Partition file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected 2 lines in {file_path}, got {len(lines)}."

    parsed_lines = [json.loads(line) for line in lines]
    for obj in parsed_lines:
        assert obj["sensor_id"] == 3, "Incorrect sensor_id in partition 3."

    temperatures = {obj["temperature"] for obj in parsed_lines}
    assert 19.8 in temperatures, "Expected temperature 19.8 not found in sensor 3 partition."
    assert 23.5 in temperatures, "Expected temperature 23.5 not found in sensor 3 partition."