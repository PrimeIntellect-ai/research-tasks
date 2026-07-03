# test_final_state.py
import os
import json
import urllib.request
import time
import pytest

def test_pids_log_and_processes():
    """Verify pids.log format and that the referenced processes are running."""
    log_path = "/home/user/pids.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in {log_path}, found {len(lines)}."

    expected_keys = {"alpha", "beta", "gamma", "haproxy"}
    found_keys = set()

    for line in lines:
        parts = line.split(":")
        assert len(parts) == 2, f"Invalid line format in {log_path}: '{line}'. Expected 'identifier:pid'."
        key, pid_str = parts

        assert key in expected_keys, f"Unexpected identifier '{key}' in {log_path}. Expected one of {expected_keys}."
        found_keys.add(key)

        assert pid_str.isdigit(), f"PID for {key} is not a valid number: '{pid_str}'."
        pid = int(pid_str)

        # Check if process is actually running
        assert os.path.exists(f"/proc/{pid}"), f"Process for '{key}' with PID {pid} is not running."

    assert found_keys == expected_keys, f"Missing identifiers in {log_path}: {expected_keys - found_keys}."

def test_haproxy_routing():
    """Verify HAProxy is load balancing across all three backend instances."""
    url = "http://127.0.0.1:9000/health"
    seen_sensors = set()

    # Send multiple requests to ensure round-robin hits all backends
    for _ in range(15):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status == 200, f"Expected HTTP status 200, got {response.status}."

                body = response.read().decode('utf-8')
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    pytest.fail(f"Response is not valid JSON: {body}")

                assert "sensor_id" in data, f"Response JSON missing 'sensor_id' key: {data}"
                assert data.get("status") == "ok", f"Expected status 'ok' in JSON, got '{data.get('status')}'."

                seen_sensors.add(data["sensor_id"])
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to HAProxy at {url}: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during HTTP request: {e}")

        time.sleep(0.1)

    expected_sensors = {"alpha", "beta", "gamma"}
    missing = expected_sensors - seen_sensors
    assert not missing, f"Load balancing failed. Did not receive responses from instances: {missing}. Seen: {seen_sensors}"