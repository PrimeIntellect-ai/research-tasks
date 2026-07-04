# test_final_state.py

import json
import subprocess
import time
import pytest
import requests

def test_pipeline_execution_and_anomalies():
    # Step 1: Trigger the pipeline
    try:
        post_resp = requests.post("http://127.0.0.1:9090/run_pipeline", timeout=10)
        assert post_resp.status_code in [200, 201, 202, 204], f"Expected success status code for POST /run_pipeline, got {post_resp.status_code}. Response: {post_resp.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service on 127.0.0.1:9090 or POST /run_pipeline timed out: {e}")

    # Give it a tiny bit of time if it's async, though it should be synchronous
    time.sleep(1)

    # Step 2: Fetch anomalies via GET
    try:
        get_resp = requests.get("http://127.0.0.1:9090/anomalies?sensor_id=1", timeout=5)
        assert get_resp.status_code == 200, f"Expected 200 OK for GET /anomalies, got {get_resp.status_code}. Response: {get_resp.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to GET /anomalies from the Go service: {e}")

    # Step 3: Verify the JSON response
    try:
        data = get_resp.json()
    except ValueError:
        pytest.fail(f"Response from GET /anomalies was not valid JSON. Response: {get_resp.text}")

    assert isinstance(data, list), f"Expected response to be a JSON array, got {type(data).__name__}"
    assert len(data) == 1, f"Expected exactly 1 anomaly, got {len(data)}. Data: {data}"

    anomaly = data[0]
    assert anomaly.get("sensor_id") == 1, f"Expected sensor_id=1, got {anomaly.get('sensor_id')}"
    assert anomaly.get("timestamp") == 6, f"Expected timestamp=6, got {anomaly.get('timestamp')}"
    assert float(anomaly.get("value")) == 20.0, f"Expected value=20.0, got {anomaly.get('value')}"
    assert float(anomaly.get("rolling_avg")) == 11.0, f"Expected rolling_avg=11.0, got {anomaly.get('rolling_avg')}"

def test_postgres_database_state():
    # Step 4: Verify the Postgres database directly
    query = "SELECT sensor_id, timestamp, value, rolling_avg FROM anomalies WHERE sensor_id = 1 ORDER BY timestamp ASC;"
    cmd = [
        "psql",
        "postgresql://postgres:password@127.0.0.1:5432/etl_db",
        "-t",
        "-A",
        "-c",
        query
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query Postgres database. Is it running and populated? Error: {e.stderr}")

    output = result.stdout.strip()
    assert output, "The 'anomalies' table is empty or missing expected records."

    # Parse the output: sensor_id|timestamp|value|rolling_avg
    rows = output.split('\n')
    assert len(rows) == 1, f"Expected exactly 1 row in DB for sensor_id=1, got {len(rows)}. Output: {output}"

    cols = rows[0].split('|')
    assert len(cols) == 4, f"Expected 4 columns in output, got {len(cols)}"

    sensor_id, timestamp, value, rolling_avg = cols
    assert int(sensor_id) == 1, f"DB sensor_id mismatch: {sensor_id}"
    assert int(timestamp) == 6, f"DB timestamp mismatch: {timestamp}"
    assert float(value) == 20.0, f"DB value mismatch: {value}"
    assert float(rolling_avg) == 11.0, f"DB rolling_avg mismatch: {rolling_avg}"