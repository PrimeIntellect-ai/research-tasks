# test_final_state.py

import json
import os
import pytest
import redis
from sklearn.metrics import r2_score

def test_process_script_exists():
    path = "/home/user/process.py"
    assert os.path.isfile(path), f"The script {path} does not exist."

def test_summary_json():
    summary_path = "/home/user/processing_summary.json"
    assert os.path.isfile(summary_path), f"The summary file {summary_path} was not found. Did the script run successfully?"

    with open(summary_path, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {summary_path} is not valid JSON.")

    expected_rows = 1850320
    expected_timestamp = 1704067200

    actual_rows = summary.get('total_valid_rows')
    actual_timestamp = summary.get('latest_timestamp')

    assert actual_rows == expected_rows, f"total_valid_rows metric failed: expected {expected_rows}, got {actual_rows}"
    assert actual_timestamp == expected_timestamp, f"latest_timestamp metric failed: expected {expected_timestamp}, got {actual_timestamp}"

def test_redis_accuracy():
    ref_path = "/app/data/reference_avgs.json"
    assert os.path.isfile(ref_path), f"Reference averages file {ref_path} is missing."

    with open(ref_path, 'r') as f:
        references = json.load(f)

    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
    except redis.ConnectionError:
        pytest.fail("Could not connect to Redis at localhost:6379. Are the services running?")

    y_true = []
    y_pred = []

    for sensor_id, expected_avg in references.items():
        key = f"sensor:{sensor_id}:avg"
        val = r.get(key)
        assert val is not None, f"Missing Redis key {key}. The script did not populate all expected sensors."

        try:
            parsed_val = float(val)
        except ValueError:
            pytest.fail(f"Value for {key} in Redis is not a valid float: {val}")

        y_true.append(float(expected_avg))
        y_pred.append(parsed_val)

    score = r2_score(y_true, y_pred)
    assert score >= 0.999, f"Accuracy metric failed: R^2 score of {score:.5f} is below the threshold of 0.999"