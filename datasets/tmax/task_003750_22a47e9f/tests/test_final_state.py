# test_final_state.py

import os
import subprocess
import requests
import time
import pytest

def test_script_fixed_unicode():
    script_path = "/app/bash-jaccard-logger-1.0/process_log.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Test the script directly with unicode sequences
    result = subprocess.run(
        [script_path, "D\u00e9fense de stationner", "d\u00e9fense de stationner ici"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed to execute: {result.stderr}"
    # "défense de stationner" (3 words) vs "défense de stationner ici" (4 words)
    # Intersection = 3, Union = 4 -> 0.75
    output = result.stdout.strip()
    assert output == "0.75", f"Expected script to output 0.75 for unicode inputs, got: {output}"

def test_http_service_unauthorized():
    url = "http://127.0.0.1:9090"
    payload = '{"message": "test", "baseline": "test"}\n'
    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the HTTP service on 127.0.0.1:9090. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized when missing Auth header, got {response.status_code}"

def test_http_service_authorized_and_processing():
    url = "http://127.0.0.1:9090"
    headers = {"Authorization": "Bearer log-auth-key-881"}
    payload = (
        '{"message": "D\\u00e9fense de stationner", "baseline": "d\\u00e9fense de stationner ici"}\n'
        '{"message": "hello world", "baseline": "hello"}\n'
    )

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the HTTP service on 127.0.0.1:9090. Is it running?")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    lines = response.text.strip().split('\n')
    assert len(lines) == 2, f"Expected 2 lines of output, got {len(lines)}"
    assert lines[0].strip() == "0.75", f"Expected first score to be 0.75, got {lines[0]}"
    assert lines[1].strip() == "0.50", f"Expected second score to be 0.50, got {lines[1]}"

def test_processed_logs_appended():
    log_file = "/tmp/processed_logs.txt"
    assert os.path.isfile(log_file), f"Log file {log_file} was not created."
    with open(log_file, 'r') as f:
        content = f.read()

    assert "0.75" in content, f"Expected 0.75 to be appended to {log_file}"

def test_aggregation_script():
    agg_script = "/home/user/aggregate.sh"
    assert os.path.isfile(agg_script), f"Aggregation script {agg_script} is missing."
    assert os.access(agg_script, os.X_OK), f"Aggregation script {agg_script} is not executable."

    # Setup a controlled state for the aggregation script
    test_log = "/tmp/processed_logs.txt"
    with open(test_log, 'w') as f:
        f.write("0.75\n0.50\n0.25\n")

    result = subprocess.run([agg_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Aggregation script failed: {result.stderr}"

    out_file = "/tmp/average_sim.txt"
    assert os.path.isfile(out_file), f"Output file {out_file} was not created by aggregation script."

    with open(out_file, 'r') as f:
        avg = f.read().strip()

    assert avg == "0.50", f"Expected average to be 0.50, got {avg}"

def test_cron_job_installed():
    result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab for user 'user'."
    assert "/home/user/aggregate.sh" in result.stdout, "Cron job for aggregate.sh is not installed for 'user'."
    assert "* * * * *" in result.stdout, "Cron job is not set to run every minute (* * * * *)."