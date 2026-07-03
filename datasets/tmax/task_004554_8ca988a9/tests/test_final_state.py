# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import subprocess
import time

def test_nginx_conf_updated():
    conf_path = '/home/user/deploy/nginx.conf'
    assert os.path.isfile(conf_path), f"{conf_path} is missing."
    with open(conf_path, 'r') as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:5001;" in content, "nginx.conf was not updated to proxy to port 5001."

def test_config_json_created():
    config_path = '/home/user/deploy/config.json'
    assert os.path.isfile(config_path), f"{config_path} is missing."
    with open(config_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{config_path} does not contain valid JSON.")
    assert data == {"status": "ok"}, f"{config_path} does not contain the expected JSON payload."

def test_services_running():
    # Check if we can reach the backend directly on 5001
    try:
        req = urllib.request.Request("http://127.0.0.1:5001/")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, "Backend app on port 5001 did not return HTTP 200."
    except Exception as e:
        pytest.fail(f"Could not connect to backend app on port 5001: {e}")

    # Check if we can reach Nginx on 8080
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, "Nginx on port 8080 did not return HTTP 200."
    except Exception as e:
        pytest.fail(f"Could not connect to Nginx on port 8080: {e}")

def test_watchdog_script():
    watchdog_path = '/home/user/watchdog.py'
    log_path = '/home/user/status.log'

    assert os.path.isfile(watchdog_path), f"{watchdog_path} is missing."

    # Record current size of log file if it exists
    initial_size = os.path.getsize(log_path) if os.path.exists(log_path) else 0

    # Run the watchdog script
    result = subprocess.run(['python3', watchdog_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Watchdog script failed to execute: {result.stderr}"

    # Check if log file was created/appended
    assert os.path.isfile(log_path), f"{log_path} was not created by the watchdog script."

    with open(log_path, 'r') as f:
        f.seek(initial_size)
        new_content = f.read()

    assert new_content == "UP\n", f"Watchdog script did not append 'UP\\n' to {log_path}. Found: {repr(new_content)}"

def test_crontab_configured():
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Ensure crontab is configured for the user."

    crontab_content = result.stdout
    assert "watchdog.py" in crontab_content, "watchdog.py is not scheduled in the user's crontab."

    # Check if it runs every minute
    # A simple check for '* * * * *' and 'python3'
    valid_cron_found = False
    for line in crontab_content.splitlines():
        if not line.strip().startswith('#') and 'watchdog.py' in line:
            parts = line.split()
            if len(parts) >= 6 and parts[:5] == ['*', '*', '*', '*', '*'] and 'python3' in line:
                valid_cron_found = True
                break

    assert valid_cron_found, "Crontab does not contain a valid entry to run watchdog.py every minute using python3."