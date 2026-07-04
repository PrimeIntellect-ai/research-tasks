# test_final_state.py

import os
import socket
import subprocess
import time
import json
import struct
import pytest

def test_attacker_ip():
    ip_file = '/home/user/attacker_ip.txt'
    assert os.path.isfile(ip_file), f"File {ip_file} is missing"

    with open(ip_file, 'r') as f:
        content = f.read().strip()

    assert content == "192.168.100.42", f"Incorrect attacker IP in {ip_file}. Expected 192.168.100.42, got {content}"

def test_worker_patch():
    worker_path = '/home/user/app/worker.py'
    assert os.path.isfile(worker_path), f"File {worker_path} is missing"

    # Start worker.py in the background
    proc = subprocess.Popen(['python3', worker_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Give it a moment to start and bind to the port
    time.sleep(1)

    try:
        # Check if it crashed immediately
        if proc.poll() is not None:
            pytest.fail("worker.py crashed immediately upon starting or failed to start.")

        # Connect to the worker
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        try:
            s.connect(('127.0.0.1', 9000))
        except Exception as e:
            pytest.fail(f"Could not connect to worker.py on 127.0.0.1:9000: {e}")

        # Send malformed payload
        malformed_payload = b'\x02\x00\x00\x00\x64' + b'{"test":"\xc3'
        s.sendall(malformed_payload)

        # Receive response
        try:
            resp_header = s.recv(5)
            assert len(resp_header) == 5, "Did not receive a complete 5-byte header in response"

            msg_type = resp_header[0]
            length = struct.unpack('>I', resp_header[1:5])[0]

            resp_data = s.recv(length)
            resp_text = resp_data.decode('utf-8')

            resp_json = json.loads(resp_text)
            expected_json = {"status": "error", "message": "Invalid payload format"}

            assert resp_json == expected_json, f"Unexpected response payload. Expected {expected_json}, got {resp_json}"

        except Exception as e:
            pytest.fail(f"Failed to receive or parse the expected error response from worker: {e}")

        finally:
            s.close()

        # Give it a moment to potentially crash
        time.sleep(0.5)

        # Check if the process is still running
        if proc.poll() is not None:
            pytest.fail("worker.py crashed after receiving the malformed payload.")

    finally:
        # Clean up the process
        proc.terminate()
        proc.wait(timeout=2)