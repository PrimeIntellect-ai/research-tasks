# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def test_nginx_listening_and_proxying():
    """Check if Nginx is listening on 8080 and correctly proxies to the mock server."""
    url = "http://127.0.0.1:8080/v2/import"
    payload = json.dumps({
        "identifier": 999,
        "display_name": "Test User",
        "is_admin": False
    }).encode('utf-8')

    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 201, f"Expected HTTP 201 Created from proxy, got {response.status}"
            body = response.read().decode('utf-8')
            assert body == "Created", "Proxy did not return the expected response body from the mock server."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy at {url} or proxy failed: {e}")

def test_migrate_script_exists():
    """Check if the bash script was created."""
    script_path = "/home/user/migrate.sh"
    assert os.path.isfile(script_path), f"Migration script not found at {script_path}"

def test_migration_results_log():
    """Check if the migration results log contains the expected output."""
    log_path = "/home/user/migration_results.log"
    assert os.path.isfile(log_path), f"Migration results log not found at {log_path}"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "ID 1: HTTP 201",
        "ID 2: HTTP 201",
        "ID 3: HTTP 201",
        "ID 4: HTTP 201"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in log, found {len(lines)}"

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} in log mismatch. Expected '{expected}', got '{lines[i]}'"