# test_final_state.py
import os
import time
import subprocess
import requests
import json

def test_server_conf():
    conf_path = os.path.expanduser("~/server.conf")
    assert os.path.exists(conf_path), f"Configuration file {conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()

    assert "PORT=8080" in content, "PORT=8080 not found in server.conf"
    assert "HIGH_LOAD_FRAMES=73" in content, "HIGH_LOAD_FRAMES=73 not found in server.conf"

def test_http_endpoints():
    # Test /health
    try:
        r = requests.get("http://127.0.0.1:8080/health", timeout=2)
        assert r.status_code == 200, f"/health returned status {r.status_code}, expected 200"
        assert "OK" in r.text, "/health body does not contain 'OK'"
    except requests.RequestException as e:
        assert False, f"Failed to connect to /health: {e}"

    # Test /report
    try:
        r = requests.get("http://127.0.0.1:8080/report", timeout=2)
        assert r.status_code == 200, f"/report returned status {r.status_code}, expected 200"
        content_type = r.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"
        try:
            data = r.json()
        except ValueError:
            assert False, f"Failed to parse JSON from /report. Raw response: {r.text}"

        assert data.get("high_load_frames") == 73, f"Expected high_load_frames to be 73, got {data.get('high_load_frames')}"
    except requests.RequestException as e:
        assert False, f"Failed to connect to /report: {e}"

def test_supervisor_and_restart():
    # Find the server process
    try:
        output = subprocess.check_output(["pgrep", "-x", "server"]).decode("utf-8")
        server_pids = [int(x) for x in output.strip().split("\n") if x]
    except subprocess.CalledProcessError:
        server_pids = []

    assert len(server_pids) > 0, "The 'server' executable is not currently running."

    server_pid = server_pids[0]

    # Kill the server process to test the supervisor script
    try:
        os.kill(server_pid, 9)
    except OSError as e:
        assert False, f"Failed to kill server process {server_pid}: {e}"

    # Wait for the supervisor to restart the server
    time.sleep(2)

    # Test /health again to verify it was restarted
    try:
        r = requests.get("http://127.0.0.1:8080/health", timeout=2)
        assert r.status_code == 200, f"After kill, /health returned status {r.status_code}"
        assert "OK" in r.text, "After kill, /health body does not contain 'OK'"
    except requests.RequestException as e:
        assert False, f"Failed to connect to /health after killing server. Supervisor script likely failed to restart it: {e}"