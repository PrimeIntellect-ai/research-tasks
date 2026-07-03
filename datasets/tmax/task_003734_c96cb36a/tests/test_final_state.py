# test_final_state.py

import os
import subprocess
import json
import time
import requests
import pytest

def test_flush_metrics_script():
    path = "/home/user/flush_metrics.sh"
    assert os.path.isfile(path), f"Expected script {path} to exist."
    assert os.access(path, os.X_OK), f"Expected {path} to be executable."

def test_crontab_configured():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."
    assert "* * * * * /home/user/flush_metrics.sh" in result.stdout, "Crontab does not contain the expected cron expression."

def test_pipeline_end_to_end():
    # Clear redis and archive file to ensure clean state
    subprocess.run(["redis-cli", "DEL", "pipeline_metrics"], capture_output=True)
    archive_path = "/home/user/data/metrics_archive.jsonl"
    if os.path.exists(archive_path):
        os.remove(archive_path)

    # 1. Send POST to ingest
    csv_payload = (
        'machine_id,timestamp,sensor_dump\n'
        'm1,2023-01-01T10:00:00Z,"System OK\n'
        'Temp: 45C\n'
        'Load: 12%\n'
        'Fan: 1200RPM"\n'
        'm2,2023-01-01T10:01:00Z,"Temp: 50C\n'
        'Load: 80%"\n'
    )

    try:
        response = requests.post("http://127.0.0.1:8080/ingest", data=csv_payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or server error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    # Check if response text indicates 5 metrics (optional, but task says return total number)
    assert "5" in response.text, f"Expected response to contain '5' (the number of metrics extracted), got: {response.text}"

    # 2. Check Redis for the metrics
    redis_res = subprocess.run(["redis-cli", "LRANGE", "pipeline_metrics", "0", "-1"], capture_output=True, text=True)
    assert redis_res.returncode == 0, "Failed to execute redis-cli."
    redis_output = redis_res.stdout.strip().split('\n')
    redis_output = [line for line in redis_output if line]

    assert len(redis_output) == 5, f"Expected 5 metrics in Redis list 'pipeline_metrics', found {len(redis_output)}."

    # Parse JSONs
    metrics = []
    for line in redis_output:
        try:
            metrics.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in Redis: {line}")

    # Check contents roughly
    metrics_str = json.dumps(metrics)
    assert "Temp" in metrics_str
    assert "Load" in metrics_str
    assert "Fan" in metrics_str
    assert "45" in metrics_str
    assert "1200" in metrics_str

    # 3. Trigger flush_metrics.sh
    flush_res = subprocess.run(["/home/user/flush_metrics.sh"], capture_output=True, text=True)
    assert flush_res.returncode == 0, f"flush_metrics.sh failed to run: {flush_res.stderr}"

    # 4. Check Redis is empty
    redis_res_after = subprocess.run(["redis-cli", "LLEN", "pipeline_metrics"], capture_output=True, text=True)
    assert redis_res_after.stdout.strip() == "0", "Expected Redis list 'pipeline_metrics' to be empty after flushing."

    # 5. Check archive file
    assert os.path.isfile(archive_path), f"Expected archive file {archive_path} to exist after flushing."
    with open(archive_path, "r") as f:
        archived_lines = [line.strip() for line in f if line.strip()]

    assert len(archived_lines) >= 5, f"Expected at least 5 metrics in archive file, found {len(archived_lines)}."