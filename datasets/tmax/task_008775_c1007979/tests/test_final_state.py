# test_final_state.py

import os
import json
import subprocess
import pytest

def test_anomaly_time():
    time_file = "/home/user/anomaly_time.txt"
    assert os.path.isfile(time_file), f"File {time_file} does not exist."
    with open(time_file, "r") as f:
        content = f.read().strip()

    assert content == "2023-11-01T10:05:05Z", f"Incorrect anomaly time extracted. Expected '2023-11-01T10:05:05Z', got '{content}'."

def test_output_json_validity_and_content():
    output_file = "/home/user/output.json"
    assert os.path.isfile(output_file), f"File {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {output_file} is not valid JSON: {content}")

    assert "batch_id" in data, "output.json missing 'batch_id' field."
    assert "variance" in data, "output.json missing 'variance' field."

    assert data["batch_id"] == "A1", f"Expected batch_id 'A1', got {data['batch_id']}"

    # Check if variance is a number (float/int) and has the correct value
    variance = data["variance"]
    assert isinstance(variance, (int, float)), f"Variance should be a numeric type, got {type(variance).__name__}"
    assert abs(variance - 34.5) < 0.001, f"Expected variance 34.5, got {variance}"

def test_go_race_condition():
    go_file = "/home/user/app/sensor_agg.go"
    input_file = "/home/user/data/input.json"
    assert os.path.isfile(go_file), f"File {go_file} does not exist."

    # Run the go code with the race detector
    cmd = ["go", "run", "-race", go_file, input_file]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check if race detector found anything
    if "WARNING: DATA RACE" in result.stderr or "WARNING: DATA RACE" in result.stdout:
        pytest.fail("Data race condition still present in sensor_agg.go.")

    # Check if compilation or execution failed
    assert result.returncode == 0, f"Go program failed to execute correctly:\n{result.stderr}"

    # Validate the output from the go program itself to ensure it is fixed
    output = result.stdout.strip()
    try:
        data = json.loads(output)
        assert data.get("variance") == 34.5, f"Go program output incorrect variance: {output}"
    except json.JSONDecodeError:
        pytest.fail(f"Go program output is not valid JSON: {output}")