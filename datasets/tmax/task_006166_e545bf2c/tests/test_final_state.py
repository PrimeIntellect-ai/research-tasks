# test_final_state.py
import os
import subprocess
import socket
import json
import time
import pytest

def test_server_fixed():
    """Test that server.py handles the poison pill without crashing and returns the correct error."""
    server_path = "/home/user/server.py"
    assert os.path.isfile(server_path), "server.py is missing"

    # Start the server
    proc = subprocess.Popen(["python3", server_path])
    time.sleep(1) # Give it time to start

    try:
        # Send poison payload
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9000))
        s.sendall(b'{"action": "update_profile", "data": "new_avatar.png"}')
        data = s.recv(1024)
        s.close()

        response = json.loads(data.decode('utf-8'))
        assert response.get("status") == "error", "Expected status: error for poison payload"
        assert response.get("reason") == "bad_request", "Expected reason: bad_request for poison payload"

        # Check if server is still alive by sending a valid ping
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect(('127.0.0.1', 9000))
        s2.sendall(b'{"action": "ping"}')
        data2 = s2.recv(1024)
        s2.close()

        response2 = json.loads(data2.decode('utf-8'))
        assert response2.get("status") == "pong", "Expected status: pong for ping payload"

        # Ensure process is still running
        assert proc.poll() is None, "Server crashed after handling requests"

    finally:
        proc.terminate()
        proc.wait()

def test_mre_js_exists_and_runs():
    """Test that mre.js exists and runs without throwing errors."""
    mre_path = "/home/user/mre.js"
    assert os.path.isfile(mre_path), "mre.js is missing"

    # We can just run it using node. It might fail to connect if server is not running, 
    # but let's just check it doesn't have syntax errors.
    result = subprocess.run(["node", "--check", mre_path], capture_output=True, text=True)
    assert result.returncode == 0, f"mre.js has syntax errors: {result.stderr}"

def test_regression_test_py_exists_and_passes():
    """Test that regression_test.py exists and passes."""
    reg_path = "/home/user/regression_test.py"
    assert os.path.isfile(reg_path), "regression_test.py is missing"

    result = subprocess.run(["python3", reg_path], capture_output=True, text=True)
    assert result.returncode == 0, f"regression_test.py failed: {result.stdout}\n{result.stderr}"