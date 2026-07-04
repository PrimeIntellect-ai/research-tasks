# test_final_state.py

import os
import socket
import struct
import base64
import subprocess
import time
import pytest

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    start_sh = "/home/user/project/start.sh"
    assert os.path.exists(start_sh), f"{start_sh} does not exist."
    assert os.access(start_sh, os.X_OK), f"{start_sh} is not executable."

    # Execute start.sh
    subprocess.run([start_sh], cwd="/home/user/project", check=True)

    # Wait for server to start
    time.sleep(3)

    yield

    # Teardown: kill the process
    pid_file = "/home/user/project/server.pid"
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            pid_str = f.read().strip()
            if pid_str.isdigit():
                try:
                    os.kill(int(pid_str), 9)
                except ProcessLookupError:
                    pass

def test_makefile_exists():
    assert os.path.exists("/home/user/project/Makefile"), "Makefile does not exist."

def test_shared_library_built():
    so_path = "/home/user/project/build/libsanitizer.so"
    assert os.path.exists(so_path), f"Shared library {so_path} was not built."

def test_server_pid_exists_and_running():
    pid_file = "/home/user/project/server.pid"
    assert os.path.exists(pid_file), "server.pid does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), "server.pid does not contain a valid integer PID."

    # Check if process is running
    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        pytest.fail(f"Process with PID {pid} is not running.")

def ws_connect(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect((host, port))
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    handshake = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(handshake.encode('utf-8'))
    resp = s.recv(4096)
    assert b"101 Switching Protocols" in resp, "WebSocket handshake failed"
    return s

def ws_send(s, text):
    payload = text.encode('utf-8')
    length = len(payload)
    header = bytearray([0x81]) # FIN + Text
    if length < 126:
        header.append(length | 0x80)
    elif length < 65536:
        header.append(126 | 0x80)
        header.extend(struct.pack("!H", length))
    else:
        header.append(127 | 0x80)
        header.extend(struct.pack("!Q", length))

    mask = os.urandom(4)
    header.extend(mask)
    masked_payload = bytearray(length)
    for i in range(length):
        masked_payload[i] = payload[i] ^ mask[i % 4]

    s.sendall(header + masked_payload)

def ws_recv(s):
    header = s.recv(2)
    if not header:
        return None
    b1, b2 = header
    opcode = b1 & 0x0f
    masked = b2 & 0x80
    length = b2 & 0x7f

    if length == 126:
        length = struct.unpack("!H", s.recv(2))[0]
    elif length == 127:
        length = struct.unpack("!Q", s.recv(8))[0]

    if masked:
        mask = s.recv(4)

    payload = b""
    while len(payload) < length:
        chunk = s.recv(length - len(payload))
        if not chunk:
            break
        payload += chunk

    if masked:
        unmasked = bytearray(length)
        for i in range(length):
            unmasked[i] = payload[i] ^ mask[i % 4]
        payload = unmasked

    return payload.decode('utf-8')

def test_websocket_server_behavior():
    try:
        ws = ws_connect("127.0.0.1", 8765)
    except Exception as e:
        pytest.fail(f"Could not connect to WebSocket server on 127.0.0.1:8765: {e}")

    # Test safe payload
    ws_send(ws, "Hello World")
    resp = ws_recv(ws)
    assert resp == "SAFE: Hello World", f"Expected 'SAFE: Hello World', got '{resp}'"

    # Test malicious payload 1
    ws_send(ws, "<script>alert(1)</script>")
    resp = ws_recv(ws)
    assert resp == "REJECTED", f"Expected 'REJECTED', got '{resp}'"

    # Test malicious payload 2
    ws_send(ws, "SELECT * FROM users WHERE id=1 OR 1=1;")
    resp = ws_recv(ws)
    assert resp == "REJECTED", f"Expected 'REJECTED', got '{resp}'"

    ws.close()