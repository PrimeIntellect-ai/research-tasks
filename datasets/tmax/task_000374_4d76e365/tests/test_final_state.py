# test_final_state.py

import os
import json
import socket
import subprocess
import requests
import pytest
import time

def test_processes_running():
    # Check if the three python services are running
    services = ["kv_store.py", "backend.py", "frontend.py"]
    for svc in services:
        result = subprocess.run(["pgrep", "-f", svc], capture_output=True, text=True)
        assert result.returncode == 0, f"Service {svc} is not running."

def test_kv_store_tcp():
    # Multi-protocol Check 1: Raw TCP
    try:
        with socket.create_connection(("127.0.0.1", 8001), timeout=5) as s:
            s.sendall(b"PING\n")
            data = s.recv(1024)
            assert b"PONG" in data, f"Expected PONG from kv_store, got {data!r}"
    except Exception as e:
        pytest.fail(f"Failed to connect to kv_store on port 8001 or receive response: {e}")

def test_frontend_http():
    # Multi-protocol Check 2: HTTP
    try:
        response = requests.get("http://127.0.0.1:8003/api/data", timeout=5)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
        data = response.json()
        assert data.get("data") == "success", f"Expected {{'data': 'success'}}, got {data}"
    except Exception as e:
        pytest.fail(f"Failed to fetch from frontend on port 8003: {e}")

def test_health_monitor_script():
    script_path = "/home/user/health_monitor.py"
    log_path = "/home/user/status.log"

    assert os.path.isfile(script_path), f"Health monitor script not found at {script_path}"

    # Run the script to ensure it generates the log
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {script_path} failed with error: {result.stderr}"

    assert os.path.isfile(log_path), f"Log file not found at {log_path} after running the script"

    with open(log_path, "r") as f:
        content = f.read()

    try:
        log_json = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {log_path} is not valid JSON: {content}")

    assert log_json.get("data") == "success", f"Expected {{'data': 'success'}} in {log_path}, got {log_json}"