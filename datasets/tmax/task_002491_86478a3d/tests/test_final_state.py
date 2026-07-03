# test_final_state.py

import os
import json
import subprocess
import time
import pytest

def test_producer_patched():
    producer_path = "/home/user/services/producer.py"
    assert os.path.isfile(producer_path), f"File {producer_path} does not exist."

    with open(producer_path, "r") as f:
        content = f.read()

    assert "/home/user/services/sockets/app.sock" in content, (
        "producer.py has not been patched to use the correct socket path "
        "(/home/user/services/sockets/app.sock)."
    )
    assert "/tmp/app.sock" not in content, (
        "producer.py still contains the old incorrect socket path (/tmp/app.sock)."
    )

def test_processes_running():
    # Give the processes a moment to be fully up if they were just started
    time.sleep(1)

    try:
        output = subprocess.check_output(["ps", "aux"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute `ps aux` to check running processes.")

    assert "consumer.py" in output, "consumer.py is not running in the background."
    assert "producer.py" in output, "producer.py is not running in the background."
    assert "monitor.py" in output, "monitor.py is not running in the background."

def test_alerts_json_schema_and_content():
    alerts_path = "/home/user/services/alerts.json"

    # Wait briefly to ensure at least one error might have been processed
    # The producer sleeps 1 sec and randomly picks from 3 messages, so an error should appear soon.
    # We will wait up to 10 seconds for the file to be created and populated.
    for _ in range(20):
        if os.path.exists(alerts_path) and os.path.getsize(alerts_path) > 0:
            break
        time.sleep(0.5)

    assert os.path.isfile(alerts_path), f"Alerts file {alerts_path} does not exist."
    assert os.path.getsize(alerts_path) > 0, f"Alerts file {alerts_path} is empty."

    # Calculate expected directory size
    data_store_dir = "/home/user/services/data_store/"
    expected_size = 0
    if os.path.exists(data_store_dir):
        for f in os.listdir(data_store_dir):
            file_path = os.path.join(data_store_dir, f)
            if os.path.isfile(file_path):
                expected_size += os.path.getsize(file_path)

    with open(alerts_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, "No JSON lines found in alerts.json."

    for line in lines:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in alerts.json: {line}")

        assert "event" in data, f"Missing 'event' key in JSON: {data}"
        assert data["event"] == "SYNC_ERROR", f"Incorrect 'event' value: {data['event']}"

        assert "data_store_size_bytes" in data, f"Missing 'data_store_size_bytes' key in JSON: {data}"
        assert isinstance(data["data_store_size_bytes"], int), "data_store_size_bytes must be an integer."
        assert data["data_store_size_bytes"] == expected_size, (
            f"Expected data_store_size_bytes to be {expected_size}, got {data['data_store_size_bytes']}"
        )