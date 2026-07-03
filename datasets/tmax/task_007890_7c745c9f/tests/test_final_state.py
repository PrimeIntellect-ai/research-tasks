# test_final_state.py
import os
import subprocess
import time
import urllib.request
import json
import socket
import base64
import signal

def wait_for_port_file(timeout=5.0):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists("/home/user/active_port.txt"):
            with open("/home/user/active_port.txt", "r") as f:
                port = f.read().strip()
                if port:
                    return port
        time.sleep(0.1)
    return None

def ws_send_receive(port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect(('127.0.0.1', int(port)))

    # Handshake
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    req = (
        f"GET / HTTP/1.1\r\n"
        f"Host: 127.0.0.1:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode())
    resp = s.recv(4096)
    assert b"101 Switching Protocols" in resp, "WebSocket handshake failed"

    # Send text frame
    msg_bytes = message.encode('utf-8')
    header = bytearray([0x81, 0x80 | len(msg_bytes)])
    mask = os.urandom(4)
    header.extend(mask)
    payload = bytearray([msg_bytes[i] ^ mask[i % 4] for i in range(len(msg_bytes))])
    s.sendall(header + payload)

    # Receive text frame
    resp = s.recv(4096)
    assert resp[0] == 0x81, "Expected text frame from WebSocket server"
    length = resp[1] & 0x7F
    payload = resp[2:2+length]
    s.close()
    return payload.decode('utf-8')

def test_script_exists_and_executable():
    script_path = "/home/user/qa_agent.py"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_legacy_lib_starts_http_server():
    if os.path.exists("/home/user/active_port.txt"):
        os.remove("/home/user/active_port.txt")

    env = os.environ.copy()
    env["TEST_LIB_PATH"] = "/home/user/libv1.so"

    p = subprocess.Popen(["python3", "/home/user/qa_agent.py"], env=env)
    try:
        port = wait_for_port_file()
        assert port == "8080", f"Expected port 8080 for v1, got {port}"

        time.sleep(1) # Give server time to bind

        req = urllib.request.urlopen("http://127.0.0.1:8080/", timeout=5.0)
        data = json.loads(req.read().decode())

        assert data.get("status") == "legacy", "Expected status 'legacy' in JSON response"
        assert data.get("version") == "1.8.5", "Expected version '1.8.5' in JSON response"
    finally:
        p.send_signal(signal.SIGINT)
        p.kill()
        p.wait()

def test_modern_lib_starts_ws_server():
    if os.path.exists("/home/user/active_port.txt"):
        os.remove("/home/user/active_port.txt")

    env = os.environ.copy()
    env["TEST_LIB_PATH"] = "/home/user/libv2.so"

    p = subprocess.Popen(["python3", "/home/user/qa_agent.py"], env=env)
    try:
        port = wait_for_port_file()
        assert port == "8081", f"Expected port 8081 for v2, got {port}"

        time.sleep(1) # Give server time to bind

        # Test hash computation via websocket
        response = ws_send_receive(8081, "10")
        assert response == "427", f"Expected 427 from websocket server, got {response}"
    finally:
        p.send_signal(signal.SIGINT)
        p.kill()
        p.wait()