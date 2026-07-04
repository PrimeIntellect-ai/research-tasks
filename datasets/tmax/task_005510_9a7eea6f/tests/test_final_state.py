# test_final_state.py
import os
import subprocess
import urllib.request
import json
import pytest
import time
import socket

def check_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def test_rust_server_running():
    assert check_port_open(8081), "Rust WebSocket server is not listening on port 8081"

def test_proxy_running():
    assert check_port_open(8080), "Reverse proxy is not listening on port 8080"

def test_proxy_pid_file():
    pid_file = "/home/user/proxy.pid"
    assert os.path.isfile(pid_file), f"{pid_file} does not exist"
    with open(pid_file, "r") as f:
        pid = f.read().strip()
    assert pid.isdigit(), f"PID file {pid_file} does not contain a valid integer PID"

    # Check if process is running
    try:
        os.kill(int(pid), 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running")

def test_websocket_behavior():
    # We will use python's websockets to test the proxy on 8080
    client_script = """
import asyncio
import websockets
import sys

async def test():
    uri = "ws://127.0.0.1:8080"
    tests = {
        'print "test"': 'test',
        '9 / 2': '4',
        'print 10 / 3': '3',
        'invalid syntax': 'ERROR'
    }
    try:
        async with websockets.connect(uri) as websocket:
            for req, expected in tests.items():
                await websocket.send(req)
                res = await websocket.recv()
                if res != expected:
                    print(f"Failed on {req}: expected {expected}, got {res}")
                    sys.exit(1)
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

asyncio.run(test())
"""
    with open("/tmp/test_ws.py", "w") as f:
        f.write(client_script)

    result = subprocess.run(["python3", "/tmp/test_ws.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"WebSocket test failed: {result.stdout}\n{result.stderr}"

def test_sorted_results():
    raw_file = "/home/user/raw_results.txt"
    sorted_file = "/home/user/sorted_results.txt"

    assert os.path.isfile(raw_file), f"{raw_file} does not exist"
    assert os.path.isfile(sorted_file), f"{sorted_file} does not exist"

    with open(raw_file, "r") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    with open(sorted_file, "r") as f:
        sorted_lines = [line.strip() for line in f if line.strip()]

    assert len(raw_lines) == len(sorted_lines), "Sorted file does not have the same number of lines as raw file"

    def get_latency(line):
        parts = line.split()
        if not parts: return -1
        try:
            return int(parts[0])
        except ValueError:
            return -1

    expected_sorted = sorted(raw_lines, key=get_latency, reverse=True)
    assert sorted_lines == expected_sorted, "Results are not correctly sorted by latency in descending order"

    # Check that expected values are present
    results_only = [" ".join(line.split()[1:]) for line in raw_lines]
    assert set(results_only) == {"hello", "2", "3", "ERROR"}, "Raw results don't contain the expected outputs"