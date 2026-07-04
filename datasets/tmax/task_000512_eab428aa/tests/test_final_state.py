# test_final_state.py

import os
import json
import time
import socket
import threading
import subprocess
import uuid
import pytest

REPORT_PATH = "/home/user/resolution_report.json"
SYSTEM_DIR = "/home/user/ticket_system"
ROUTER_SCRIPT = os.path.join(SYSTEM_DIR, "ticket_router.py")
LOG_FILE = os.path.join(SYSTEM_DIR, "processed_tickets.log")

def test_resolution_report_exists_and_valid():
    """Validates the existence, structure, and correctness of the JSON report."""
    assert os.path.isfile(REPORT_PATH), f"The resolution report is missing at {REPORT_PATH}."

    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file at {REPORT_PATH} does not contain valid JSON.")

    # Check structure
    assert "missing_ticket_id" in data, "The report is missing the 'missing_ticket_id' key."
    assert "master_token" in data, "The report is missing the 'master_token' key."

    # Validate Phase 1 & 2 answers
    # TKT-1003 is the only ticket in the pcap (1001-1005) missing from the initial log
    expected_missing_ticket = "TKT-1003"
    # The master token hardcoded in auth_checker.c
    expected_master_token = "OVR-9982-ADMIN-SYS"

    assert data["missing_ticket_id"] == expected_missing_ticket, \
        f"Incorrect missing_ticket_id. Expected {expected_missing_ticket}, got {data['missing_ticket_id']}."

    assert data["master_token"] == expected_master_token, \
        f"Incorrect master_token recovered. Expected {expected_master_token}, got {data['master_token']}."

def test_ticket_router_concurrency_fix():
    """Validates that the race conditions in ticket_router.py are fixed under concurrent load."""
    assert os.path.isfile(ROUTER_SCRIPT), f"The script {ROUTER_SCRIPT} is missing."

    # Start the ticket router server
    server_proc = subprocess.Popen(
        ["python3", "ticket_router.py"], 
        cwd=SYSTEM_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        # Wait for the server to bind to port 8888
        port_open = False
        for _ in range(20):
            try:
                with socket.create_connection(("127.0.0.1", 8888), timeout=0.1):
                    port_open = True
                    break
            except OSError:
                time.sleep(0.1)

        assert port_open, "The ticket_router.py server did not start or bind to 127.0.0.1:8888 within 2 seconds."

        # Prepare 50 unique requests to test concurrency
        # A valid token is 10 characters long based on auth_checker.c fallback logic
        test_ids = [f"TEST-CONC-{uuid.uuid4().hex[:8]}" for _ in range(50)]
        errors = []

        def send_ticket(t_id):
            try:
                s = socket.create_connection(("127.0.0.1", 8888), timeout=2)
                payload = json.dumps({"id": t_id, "token": "1234567890"})
                s.sendall(payload.encode('utf-8'))
                resp = s.recv(1024)
                if resp != b"OK":
                    errors.append(f"Unexpected response for {t_id}: {resp}")
                s.close()
            except Exception as e:
                errors.append(f"Connection/Transmission error for {t_id}: {e}")

        # Launch 50 concurrent threads
        threads = []
        for t_id in test_ids:
            t = threading.Thread(target=send_ticket, args=(t_id,))
            threads.append(t)
            t.start()

        # Wait for all client threads to finish
        for t in threads:
            t.join()

        assert not errors, f"Errors occurred during concurrent request transmission: {errors[:3]}"

    finally:
        # Ensure the server process is terminated
        server_proc.terminate()
        try:
            server_proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_proc.kill()

    # Validate the log file to ensure no tickets were dropped
    assert os.path.isfile(LOG_FILE), f"The log file {LOG_FILE} is missing."

    with open(LOG_FILE, "r") as f:
        log_content = f.read()

    missing_ids = [t_id for t_id in test_ids if t_id not in log_content]

    assert not missing_ids, (
        f"Race condition is not fixed! {len(missing_ids)} out of 50 concurrent tickets were dropped "
        f"from {LOG_FILE}. Missing examples: {missing_ids[:3]}"
    )