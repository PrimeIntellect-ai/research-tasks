# test_final_state.py

import os
import subprocess
import time
import json
import urllib.request
import urllib.error
import pytest

def test_detector_adversarial_corpus():
    detector_script = "/home/user/detector.py"
    assert os.path.isfile(detector_script), f"Detector script not found at {detector_script}"

    evil_dir = "/home/user/corpora/evil"
    clean_dir = "/home/user/corpora/clean"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.jsonl')]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.jsonl')]

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", detector_script, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", detector_script, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_messages, " ; ".join(error_messages)

def test_end_to_end_telemetry_flow():
    # Start the services
    start_script = "/home/user/app/start_services.sh"
    assert os.path.isfile(start_script), f"Start script not found at {start_script}"

    # We run the script in the background
    process = subprocess.Popen(["bash", start_script], cwd="/home/user/app", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for services to be up
    time.sleep(5)

    try:
        # Send a POST request to the Flask API
        req_data = json.dumps({
            "event_id": "test-12345",
            "start_time": "2023-10-15T14:30:00Z",
            "end_time": "2023-10-15T14:30:05Z"
        }).encode('utf-8')

        req = urllib.request.Request(
            "http://localhost:5000/ingest",
            data=req_data,
            headers={'Content-Type': 'application/json'}
        )

        try:
            with urllib.request.urlopen(req) as response:
                assert response.status == 200, f"Expected status 200, got {response.status}"
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to Flask API: {e}")

        # Wait for worker to process
        time.sleep(2)

        # Check the processed_events.log
        log_file = "/home/user/app/processed_events.log"
        assert os.path.isfile(log_file), f"Log file {log_file} was not created."

        with open(log_file, "r") as f:
            logs = f.read()

        assert "test-12345" in logs, "The test event was not found in the processed logs."

        # Ensure duration is positive (5 seconds)
        # We don't strictly parse the exact format, but ensure it's successfully logged
        # and doesn't contain negative duration if the student logs it.
        assert "-5" not in logs, "Negative duration found in logs."

    finally:
        # Cleanup processes
        subprocess.run(["pkill", "-f", "api.py"])
        subprocess.run(["pkill", "-f", "worker.py"])
        subprocess.run(["pkill", "-f", "redis-server"])