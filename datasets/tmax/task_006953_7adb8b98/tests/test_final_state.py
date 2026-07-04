# test_final_state.py

import os
import socket
import subprocess
import time
import pytest

def send_tcp_message(port, message):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=2) as s:
            s.sendall(message.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response.strip()
    except Exception:
        return None

def check_process_running(cmd_substring):
    try:
        output = subprocess.check_output(["pgrep", "-f", cmd_substring], text=True)
        return len(output.strip().split('\n')) > 0
    except subprocess.CalledProcessError:
        return False

def test_files_exist():
    expected_files = [
        "/home/user/src/worker.cpp",
        "/home/user/bin/worker",
        "/home/user/nginx/nginx.conf",
        "/home/user/monitor.py",
        "/home/user/deploy.sh"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Expected file {f} does not exist."

def test_processes_running():
    assert check_process_running("nginx"), "Nginx process is not running."
    assert check_process_running("monitor.py"), "Monitor process is not running."
    for port in ["9001", "9002", "9003"]:
        assert check_process_running(f"worker {port}"), f"Worker process for port {port} is not running."

def test_nginx_proxy_round_robin():
    responses = set()
    for _ in range(5):
        resp = send_tcp_message(8080, "VERSION\n")
        assert resp is not None, "Failed to connect to Nginx proxy on port 8080 or no response."
        assert resp.startswith("v2_"), f"Unexpected response from worker: {resp}"
        responses.add(resp)

    assert len(responses) >= 2, "Nginx does not appear to be load balancing across multiple instances."

def test_monitor_revives_worker():
    # Kill the worker on port 9002
    subprocess.run(["pkill", "-f", "worker 9002"])

    # Verify it is dead
    assert not check_process_running("worker 9002"), "Failed to kill worker 9002 for testing."

    # Wait for the monitor to restart it (checks every 2 seconds, wait 5 to be safe)
    time.sleep(5)

    # Verify it is revived
    assert check_process_running("worker 9002"), "Monitor failed to revive worker 9002."

    # Verify it responds to PING
    resp = send_tcp_message(9002, "PING\n")
    assert resp == "PONG", f"Revived worker 9002 did not respond with PONG, got: {resp}"