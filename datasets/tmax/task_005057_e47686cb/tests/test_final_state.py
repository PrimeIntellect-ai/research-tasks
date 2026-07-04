# test_final_state.py

import os
import re
import json
import socket
import subprocess
import requests
import pytest

def test_server_py_fixed():
    """Test that the server.py file has been fixed to use METRICS_PORT."""
    server_file = "/app/vendor/metrics_server-1.0.0/server.py"
    assert os.path.isfile(server_file), f"File {server_file} is missing"
    with open(server_file, "r") as f:
        content = f.read()

    assert "METRICS_PORT" in content, "The server.py file was not fixed to use METRICS_PORT."

def test_gather_stats_script_exists():
    """Test that the gather_stats.py script exists."""
    script_file = "/home/user/gather_stats.py"
    assert os.path.isfile(script_file), f"File {script_file} is missing"

def test_stats_json_exists_and_valid():
    """Test that stats.json exists and contains the correct JSON structure."""
    stats_file = "/home/user/stats.json"
    assert os.path.isfile(stats_file), f"File {stats_file} is missing"

    with open(stats_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("stats.json does not contain valid JSON")

    assert "process_count" in data, "stats.json is missing the 'process_count' key"
    assert isinstance(data["process_count"], int), "'process_count' is not an integer"

def test_cron_job_configured():
    """Test that the cron job for gather_stats.py is configured."""
    try:
        crontab_output = subprocess.check_output(["crontab", "-l", "-u", "user"], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError:
        try:
            crontab_output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT).decode()
        except subprocess.CalledProcessError:
            pytest.fail("Failed to read crontab")

    assert "gather_stats.py" in crontab_output, "Cron job for gather_stats.py is not configured"

def test_http_metrics_server():
    """Test that the metrics server is running on port 9090 and returns valid JSON."""
    try:
        response = requests.get("http://127.0.0.1:9090/", timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to metrics server on port 9090: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from metrics server is not valid JSON: {response.text}")

    assert "process_count" in data, "JSON response missing 'process_count' key"
    assert isinstance(data["process_count"], int), "'process_count' in JSON response is not an integer"

def test_tcp_aggregator():
    """Test that the TCP aggregator is running on port 8080 and responds correctly."""
    host = "127.0.0.1"
    port = 8080

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((host, port))
            s.sendall(b"FETCH_CAPACITY\n")
            response = s.recv(1024).decode("utf-8")
    except Exception as e:
        pytest.fail(f"Failed to communicate with TCP aggregator on port 8080: {e}")

    assert re.match(r"^CAPACITY_OK: \d+\n$", response), f"Invalid response from TCP aggregator: {repr(response)}"