# test_final_state.py

import os
import time
import json
import random
import subprocess
import urllib.request
import pytest

def test_fuzz_parser():
    """
    Fuzz-equivalence test: compares the agent's log_parser.py against the oracle_parser
    for 1000 random 16-character hex strings.
    """
    random.seed(42)
    hex_chars = "0123456789abcdef"

    for _ in range(1000):
        hex_str = "".join(random.choices(hex_chars, k=16))

        # Run oracle
        oracle_proc = subprocess.run(
            ["/app/oracle_parser", hex_str],
            capture_output=True, text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {hex_str}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", "/app/log_parser.py", hex_str],
            capture_output=True, text=True
        )
        assert agent_proc.returncode == 0, f"Agent parser failed on input {hex_str}. Error: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on input {hex_str}:\n"
            f"Oracle: {oracle_out}\n"
            f"Agent : {agent_out}"
        )

def test_ports_fixed():
    """
    Verify that the incorrect port 6380 has been removed from the service files.
    """
    for filepath in ["/app/api.py", "/app/worker.py"]:
        assert os.path.isfile(filepath), f"File not found: {filepath}"
        with open(filepath, "r") as f:
            content = f.read()
        assert "6380" not in content, f"Incorrect port 6380 is still present in {filepath}"

def test_end_to_end_flow():
    """
    End-to-end multi-service test: starts the API and Worker, sends a POST request,
    and verifies the final processed output in processed_logs.json.
    """
    # Ensure redis is running (it should be, but just in case)
    subprocess.run(["redis-server", "--daemonize", "yes"], capture_output=True)

    # Start the Flask API and Worker as subprocesses to ensure they run the latest code
    api_proc = subprocess.Popen(["python3", "/app/api.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    worker_proc = subprocess.Popen(["python3", "/app/worker.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Wait for services to initialize
        time.sleep(2)

        # Send POST request to ingest
        payload = json.dumps({"log": "ffffffffffffffff"}).encode("utf-8")
        req = urllib.request.Request(
            "http://localhost:5000/ingest",
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req) as response:
                assert response.status == 200, f"Expected HTTP 200, got {response.status}"
        except Exception as e:
            pytest.fail(f"Failed to communicate with Flask API: {e}")

        # Wait for the worker to process the queue
        time.sleep(2)

        log_file = "/app/processed_logs.json"
        assert os.path.exists(log_file), f"Expected output file {log_file} was not created."

        with open(log_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        assert len(lines) > 0, f"Output file {log_file} is empty."

        last_log = json.loads(lines[-1])
        assert last_log.get("event_id") == 4294967295, f"Incorrect event_id in E2E test: {last_log.get('event_id')}"
        assert last_log.get("duration_ms") == 4294967295, f"Incorrect duration_ms in E2E test: {last_log.get('duration_ms')}"

    finally:
        api_proc.terminate()
        worker_proc.terminate()
        api_proc.wait()
        worker_proc.wait()