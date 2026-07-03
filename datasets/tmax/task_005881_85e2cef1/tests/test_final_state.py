# test_final_state.py

import os
import json
import math

def test_metrics_json():
    """Test that metrics.json exists and contains the correct calculated values."""
    path = '/home/user/output/metrics.json'
    assert os.path.isfile(path), f"File {path} does not exist. Did the Go program run successfully?"

    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"File {path} is not valid JSON."

    assert 'aligned_points' in data, "Missing 'aligned_points' key in JSON output."
    assert data['aligned_points'] == 3, f"Expected 3 aligned points, got {data['aligned_points']}."

    assert 'distance' in data, "Missing 'distance' key in JSON output."
    expected_distance = 0.5744562646538029
    actual_distance = data['distance']
    assert isinstance(actual_distance, (int, float)), "Distance must be a number."
    assert math.isclose(actual_distance, expected_distance, abs_tol=0.001), \
        f"Calculated distance {actual_distance} is not within 0.001 of expected {expected_distance}."

def test_run_pipeline_executable():
    """Test that run_pipeline.sh exists and is executable."""
    path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable. Run 'chmod +x {path}'."

def test_pipeline_cron():
    """Test that pipeline.cron exists and contains the correct cron expression."""
    path = '/home/user/pipeline.cron'
    assert os.path.isfile(path), f"Cron file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
    assert len(lines) == 1, f"Expected exactly one active cron line in {path}, found {len(lines)}."

    line = lines[0]
    assert '/home/user/run_pipeline.sh' in line, f"Cron line does not execute /home/user/run_pipeline.sh. Line: {line}"

    parts = line.split()
    assert len(parts) >= 6, f"Cron line does not have enough fields (expected at least 6). Line: {line}"

    minute_field = parts[0]
    valid_minutes = ['*/15', '0,15,30,45']
    assert minute_field in valid_minutes, \
        f"Minute field '{minute_field}' does not schedule every 15 minutes. Expected '*/15' or '0,15,30,45'."

    assert parts[1:5] == ['*', '*', '*', '*'], \
        f"Cron line scheduling fields (hour, day, month, dow) should be '* * * *'. Got: {' '.join(parts[1:5])}"