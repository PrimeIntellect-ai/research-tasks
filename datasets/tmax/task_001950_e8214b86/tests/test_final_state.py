# test_final_state.py

import os
import time
import subprocess
import requests
import pytest

def test_backups_exist():
    nginx_backup = '/app/backups/nginx.conf'
    app_backup = '/app/backups/app.py'

    assert os.path.isfile(nginx_backup), f"Backup {nginx_backup} is missing"
    assert os.path.isfile(app_backup), f"Backup {app_backup} is missing"

    with open(nginx_backup, 'r') as f:
        nginx_content = f.read()
    assert "proxy_pass http://127.0.0.1:5001;" in nginx_content, "Backup nginx.conf does not contain the original intentional error"

    with open(app_backup, 'r') as f:
        app_content = f.read()
    assert "por=5000" in app_content, "Backup app.py does not contain the original intentional typo"

def test_monitor_script_exists():
    assert os.path.isfile('/app/monitor.py'), "/app/monitor.py is missing"

def test_web_application_responses():
    # Test the root endpoint
    try:
        res = requests.get('http://127.0.0.1:8080/', timeout=5)
        assert res.status_code == 200, f"Expected status 200, got {res.status_code}"
        assert res.json() == {"status": "ok"}, f"Expected {{'status': 'ok'}}, got {res.json()}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to http://127.0.0.1:8080/: {e}")

    # Test the health endpoint
    try:
        res = requests.get('http://127.0.0.1:8080/health', timeout=5)
        assert res.status_code == 200, f"Expected status 200, got {res.status_code}"
        assert res.json() == {"health": "good"}, f"Expected {{'health': 'good'}}, got {res.json()}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to http://127.0.0.1:8080/health: {e}")

def test_monitor_restarts_backend():
    # Kill the backend process
    subprocess.run(["pkill", "-f", "python3 /app/app.py"], check=False)

    # Wait for the monitor to detect and restart it (monitor checks every 3 seconds)
    time.sleep(10)

    # Test the health endpoint again
    try:
        res = requests.get('http://127.0.0.1:8080/health', timeout=5)
        assert res.status_code == 200, f"Expected status 200 after restart, got {res.status_code}"
        assert res.json() == {"health": "good"}, f"Expected {{'health': 'good'}} after restart, got {res.json()}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to http://127.0.0.1:8080/health after killing backend. Monitor did not restart it properly: {e}")