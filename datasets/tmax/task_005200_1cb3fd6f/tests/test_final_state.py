# test_final_state.py

import os
import time
import requests
import pytest

def test_repro_script_exists():
    """Verify that the user created the minimal reproducible example script."""
    assert os.path.isfile("/home/user/repro.py"), "/home/user/repro.py is missing. You must create a script to reproduce the issue."

def test_system_processes_payload_correctly():
    """
    Verify that the API is running, accepts payloads, and the Node.js processor
    correctly processes deeply nested errors without hanging, appending the result
    to processed.log.
    """
    payload = {
        "event": "test_event",
        "error": {
            "message": "DB Connection Failed",
            "cause": {
                "message": "Timeout"
            }
        }
    }

    try:
        response = requests.post("http://127.0.0.1:8000/submit_log", json=payload, timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to send POST request to API. Is the API running? Error: {e}")

    # Allow some time for the Node.js processor to pick up the message from Redis and process it
    time.sleep(2)

    log_path = "/app/logs/processed.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. The processor might not be running or failed to create the log file."

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_line = "Event: test_event | Chain: DB Connection Failed -> Timeout"
    assert expected_line in log_content, (
        f"Expected line not found in {log_path}.\n"
        f"Expected to find: '{expected_line}'\n"
        f"Actual content:\n{log_content}\n\n"
        "This indicates the processor is either still hanging (bug not fixed) or processing the chain incorrectly."
    )