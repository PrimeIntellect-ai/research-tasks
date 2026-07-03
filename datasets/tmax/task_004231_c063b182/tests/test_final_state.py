# test_final_state.py

import os
import time
import requests
import pytest

def test_health_endpoint():
    """Verify that the health endpoint is reachable and returns the correct JSON."""
    url = "http://127.0.0.1:9090/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to health endpoint at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Content: {response.text}")

    assert data == {"status": "ok"}, f"Expected JSON {{'status': 'ok'}}, got {data}"

def test_metrics_endpoint():
    """Verify that the metrics endpoint is reachable and returns HTTP 200."""
    url = "http://127.0.0.1:9090/metrics"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to metrics endpoint at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

def test_backup_exists_and_updates():
    """Verify that the backup file exists and is periodically updated."""
    backup_path = "/home/user/backups/data_backup.db"
    db_path = "/home/user/data.db"

    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

    mtime1 = os.path.getmtime(backup_path)

    # Touch the source file to ensure its mtime changes, in case the backup script preserves mtimes
    if os.path.exists(db_path):
        os.utime(db_path, None)

    # Wait for 3 seconds to allow the 2-second periodic backup task to run
    time.sleep(3.0)

    mtime2 = os.path.getmtime(backup_path)
    assert mtime2 > mtime1, f"Backup file {backup_path} was not updated within 3 seconds. Ensure the backup task runs every 2 seconds."

def test_makefile_fixed():
    """Verify that the Makefile syntax error (spaces instead of tabs) has been fixed."""
    path = "/app/metrics-aggregator-1.2.0/Makefile"
    assert os.path.isfile(path), f"Makefile not found at {path}"

    with open(path, "r") as f:
        lines = f.readlines()

    run_target_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("run:"):
            run_target_idx = i
            break

    assert run_target_idx != -1, f"Makefile at {path} is missing the 'run:' target."

    # Check the next non-empty line after the run: target
    for i in range(run_target_idx + 1, len(lines)):
        line = lines[i]
        if line.strip():
            assert line.startswith("\t"), f"Makefile 'run:' target commands must be indented with a tab, found spaces."
            break

def test_config_fixed():
    """Verify that the DB_PORT in config.py is correctly set to 8080."""
    path = "/app/metrics-aggregator-1.2.0/config.py"
    assert os.path.isfile(path), f"Config file not found at {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "8080" in content, f"Expected DB_PORT to be set to 8080 in {path}."
    assert "8081" not in content, f"Incorrect port 8081 is still present in {path}."