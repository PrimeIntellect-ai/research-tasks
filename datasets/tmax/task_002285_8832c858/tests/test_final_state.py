# test_final_state.py

import os
import json
import time
import uuid
import pytest
import requests

def test_regression_test_script_exists():
    script_path = '/home/user/log_pipeline/regression_test.py'
    assert os.path.isfile(script_path), f"Expected regression test script at {script_path} is missing."

def test_pipeline_accuracy():
    """
    Tests the end-to-end log processing pipeline by pushing 10,000 log events
    with millisecond timestamps and verifying the calculated latencies.
    """
    payload = []
    run_id = str(uuid.uuid4())
    total_expected = 10000

    # Generate 10,000 log events with ms timestamps
    for i in range(total_expected):
        payload.append({
            "id": f"req-{run_id}-{i}",
            "start_ts": 1700000000000 + i,
            "end_ts": 1700000000000 + i + 50
        })

    # Push to Flask API
    try:
        response = requests.post("http://127.0.0.1:5000/logs", json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        pytest.fail(f"Failed to post logs to API: {e}. Is the Flask app running?")

    # Wait for worker to process the batch
    time.sleep(3)

    output_file = "/home/user/log_pipeline/output/metrics.json"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist. Did the worker run?"

    try:
        with open(output_file, "r") as f:
            lines = f.readlines()

        correct = 0

        for line in lines:
            if not line.strip():
                continue
            data = json.loads(line)
            # Only evaluate logs from this test run
            if data.get("id", "").startswith(f"req-{run_id}-"):
                if data.get("latency") == 50:
                    correct += 1

        accuracy = correct / float(total_expected)

        assert accuracy >= 0.99, (
            f"Accuracy metric is {accuracy} ({correct}/{total_expected} correct), "
            f"expected >= 0.99. The worker is likely still suffering from integer overflow "
            f"or dropping records."
        )

    except AssertionError:
        raise
    except Exception as e:
        pytest.fail(f"Error evaluating metric from {output_file}: {e}")