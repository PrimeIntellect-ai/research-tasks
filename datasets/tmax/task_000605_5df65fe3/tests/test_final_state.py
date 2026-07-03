# test_final_state.py

import os
import time
import subprocess
import pytest
import psycopg2
import redis

def test_process_script_execution_and_metrics():
    script_path = "/home/user/process.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the script and measure execution time
    start_time = time.time()
    res = subprocess.run(["/bin/bash", script_path], capture_output=True, text=True)
    duration = time.time() - start_time

    assert res.returncode == 0, f"process.sh failed with return code {res.returncode}.\nStdout: {res.stdout}\nStderr: {res.stderr}"
    assert duration <= 10.0, f"Execution too slow: {duration:.2f}s (Threshold: <= 10.0s)"

    # Verify PostgreSQL state
    try:
        conn = psycopg2.connect(dbname="sensor_db", user="postgres", host="localhost")
        cur = conn.cursor()
    except Exception as e:
        pytest.fail(f"Failed to connect to PostgreSQL: {e}")

    try:
        cur.execute("SELECT COUNT(*) FROM raw_data;")
        raw_count = cur.fetchone()[0]
        assert raw_count == 500000, f"Expected 500000 rows in raw_data, got {raw_count}"
    except psycopg2.Error as e:
        pytest.fail(f"Database error when querying raw_data: {e}")

    try:
        cur.execute("SELECT COUNT(*) FROM sensor_features;")
        features_count = cur.fetchone()[0]
        assert features_count == 500000, f"Expected 500000 rows in sensor_features, got {features_count}"
    except psycopg2.Error as e:
        pytest.fail(f"Database error when querying sensor_features: {e}")

    # Verify Redis state
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
    except Exception as e:
        pytest.fail(f"Failed to connect to Redis: {e}")

    keys = r.keys('sensor:*')
    assert len(keys) > 0, "No keys matching 'sensor:*' found in Redis."

    # Check a sample of values to ensure they are valid numbers and rounded to 2 decimal places
    for k in keys[:50]:
        val = r.get(k)
        try:
            float(val)
            if '.' in val:
                decimals = len(val.split('.')[-1])
                assert decimals <= 2, f"Value {val} for key {k} is not rounded to 2 decimal places."
        except ValueError:
            pytest.fail(f"Redis key {k} has non-numeric value: {val}")