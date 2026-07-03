# test_final_state.py

import os
import time
import socket
import subprocess
import signal
import pytest

def start_backend(port, response_text):
    script = f"""
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', {port}))
s.listen(5)
while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    if not data: break
    conn.sendall(b"{response_text}")
    conn.close()
"""
    return subprocess.Popen(['python3', '-c', script])

def wait_for_port(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(1)
    return False

def test_supervisor_script_exists():
    path = "/home/user/supervisor.sh"
    assert os.path.isfile(path), f"Supervisor script {path} does not exist"
    assert os.access(path, os.X_OK), f"Supervisor script {path} is not executable"

def test_rust_project_exists():
    assert os.path.isfile("/home/user/tcp_lb/Cargo.toml"), "Rust project Cargo.toml not found at /home/user/tcp_lb/Cargo.toml"
    assert os.path.isfile("/home/user/tcp_lb/src/main.rs"), "Rust source file not found at /home/user/tcp_lb/src/main.rs"

def test_proxy_functionality():
    # Start backends 1 and 3 (Simulate 2 being down)
    b1 = start_backend(9001, "BACKEND_1")
    b3 = start_backend(9003, "BACKEND_3")

    time.sleep(1) # wait for backends to bind

    # Start supervisor
    supervisor = subprocess.Popen(['/bin/bash', '/home/user/supervisor.sh'], preexec_fn=os.setsid)

    try:
        # Wait for the proxy to compile and start listening
        assert wait_for_port(9000, timeout=60), "Proxy did not start listening on port 9000 within 60 seconds"

        results = []
        for i in range(4):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2.0)
                s.connect(('127.0.0.1', 9000))
                s.sendall(b"HELLO\n")
                resp = s.recv(1024).decode()
                results.append(resp)
                s.close()
            except Exception as e:
                pass
            time.sleep(0.5)

        assert "BACKEND_1" in results, "Did not receive response from Backend 1, routing may be broken"
        assert "BACKEND_3" in results, "Did not receive response from Backend 3, routing or failover may be broken"

        with open('/home/user/diagnostics.log', 'r') as f:
            logs = f.read()

        assert "FAIL: 127.0.0.1:9002" in logs, "Did not correctly log the failed backend 'FAIL: 127.0.0.1:9002' to diagnostics.log"

    finally:
        b1.terminate()
        b3.terminate()
        try:
            os.killpg(os.getpgid(supervisor.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass