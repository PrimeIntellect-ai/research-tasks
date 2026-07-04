# test_final_state.py
import os
import subprocess
import time
import pytest

def test_payload_exists_and_executable():
    payload_path = "/home/user/payload.sh"
    assert os.path.isfile(payload_path), f"Payload script not found at {payload_path}"
    assert os.access(payload_path, os.X_OK), f"Payload script at {payload_path} is not executable"

def test_payload_execution_and_evasion():
    payload_path = "/home/user/payload.sh"
    hids_path = "/home/user/hids_monitor.sh"
    success_log = "/home/user/success.log"
    alert_log = "/home/user/IDS_ALERT"

    # Cleanup previous runs
    if os.path.exists(success_log):
        os.remove(success_log)
    if os.path.exists(alert_log):
        os.remove(alert_log)

    # Start HIDS monitor
    hids_process = subprocess.Popen([hids_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Give HIDS a moment to start
        time.sleep(0.5)

        # Run the student's payload
        result = subprocess.run([payload_path], capture_output=True, text=True, timeout=10)

        # Give HIDS a moment to catch any late writes
        time.sleep(0.5)

        # Check for success
        assert os.path.isfile(success_log), "success.log was not created. The payload did not successfully submit the correct password."
        with open(success_log, "r") as f:
            content = f.read().strip()
        assert "FLAG_COMPLETED_SUCCESSFULLY" in content, f"success.log did not contain the expected success flag. Content: {content}"

        # Check for evasion
        assert not os.path.exists(alert_log), "IDS_ALERT file was created! The payload failed to evade the HIDS monitor."

    finally:
        # Cleanup HIDS monitor
        hids_process.terminate()
        hids_process.wait(timeout=2)