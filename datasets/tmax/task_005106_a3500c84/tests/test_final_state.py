# test_final_state.py
import os
import socket
import subprocess
import time
import pytest

def test_leak_report():
    report_path = "/home/user/leak_report.txt"
    assert os.path.exists(report_path), f"File {report_path} does not exist."
    with open(report_path, "r") as f:
        content = f.read().strip()
    assert content == "1024", f"Expected leak report to contain '1024', but found '{content}'."

def test_server_sh_exists():
    script_path = "/home/user/server.sh"
    assert os.path.exists(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def send_and_receive(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        s.connect((host, port))
        s.sendall(message.encode('utf-8'))
        data = s.recv(1024)
        return data.decode('utf-8').strip()

def test_network_service():
    host = "127.0.0.1"
    port = 9000

    # Check if port is open, if not start the server
    is_open = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        if s.connect_ex((host, port)) == 0:
            is_open = True

    if not is_open:
        script_path = "/home/user/server.sh"
        assert os.path.exists(script_path), f"Server not running and {script_path} not found."
        subprocess.Popen([script_path], start_new_session=True)
        time.sleep(2)

        # Check again
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            assert s.connect_ex((host, port)) == 0, "Failed to connect to port 9000 even after starting server.sh"

    test_cases = [
        ("10 5 +\n", "RESULT: 15"),
        ("3 4 * 2 -\n", "RESULT: 10"),
        ("10 0 /\n", "ERROR: DIV0"),
        ("100 5 / 4 *\n", "RESULT: 80")
    ]

    for payload, expected in test_cases:
        try:
            response = send_and_receive(host, port, payload)
            assert response == expected, f"Sent '{payload.strip()}', expected '{expected}', but got '{response}'"
        except Exception as e:
            pytest.fail(f"Network interaction failed for payload '{payload.strip()}': {e}")