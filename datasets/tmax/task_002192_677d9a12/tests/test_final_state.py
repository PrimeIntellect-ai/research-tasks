# test_final_state.py
import os
import time
import requests
import pytest

def test_supervisor_exists():
    assert os.path.isfile('/home/user/supervisor.py'), "Supervisor script not found at /home/user/supervisor.py"

def test_log_dir_exists():
    assert os.path.isdir('/home/user/logs'), "Logs directory not found at /home/user/logs"

def test_health_endpoint():
    try:
        resp = requests.get('http://127.0.0.1:8080/health', timeout=2)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        assert resp.json() == {"status": "ok"}, f"Expected {{'status': 'ok'}}, got {resp.json()}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /health: {e}")

def test_costs_endpoint():
    try:
        resp = requests.get('http://127.0.0.1:8080/costs', timeout=2)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        assert "total_optimized_cost" in data, "Missing 'total_optimized_cost' in response"
        assert float(data["total_optimized_cost"]) == 1245.0, f"Expected 1245.0, got {data['total_optimized_cost']}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /costs: {e}")

def test_crash_and_restart():
    # Trigger crash
    try:
        requests.get('http://127.0.0.1:8080/crash', timeout=2)
    except requests.exceptions.RequestException:
        pass # Expected to drop connection or error

    # Wait for the supervisor to restart the process (must be within 3 seconds)
    time.sleep(5)

    # Check health again to verify it restarted
    try:
        resp = requests.get('http://127.0.0.1:8080/health', timeout=2)
        assert resp.status_code == 200, f"Expected 200 after restart, got {resp.status_code}"
        assert resp.json() == {"status": "ok"}, f"Expected {{'status': 'ok'}} after restart, got {resp.json()}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Service did not restart successfully after crash: {e}")

def test_log_rotation():
    # Spam requests to generate stdout/stderr logs and trigger rotation
    rotated = False
    for _ in range(50):
        for _ in range(100):
            try:
                requests.get('http://127.0.0.1:8080/health', timeout=0.5)
            except requests.exceptions.RequestException:
                pass

        # Check if the rotated log file exists
        if os.path.isfile('/home/user/logs/dashboard.log.1'):
            rotated = True
            break

    assert os.path.isfile('/home/user/logs/dashboard.log'), "Base log file /home/user/logs/dashboard.log not found"
    assert rotated, "Log rotation failed, /home/user/logs/dashboard.log.1 not found after generating many requests"