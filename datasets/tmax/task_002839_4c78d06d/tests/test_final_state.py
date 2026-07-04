# test_final_state.py

import os
import socket
import base64
import json
import pytest

def ws_connect(host, port, path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((host, port))
    except Exception as e:
        pytest.fail(f"Failed to connect to {host}:{port}: {e}")

    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode('utf-8'))
    resp = s.recv(4096)
    if b"101 Switching Protocols" not in resp:
        pytest.fail(f"WebSocket handshake failed. Response: {resp}")
    return s

def ws_send(s, text):
    msg = text.encode('utf-8')
    if len(msg) > 125:
        pytest.fail("Test message too long for simple WS client")

    mask_key = os.urandom(4)
    header = bytearray([0x81, 0x80 | len(msg)])
    header.extend(mask_key)

    masked_msg = bytearray(len(msg))
    for i in range(len(msg)):
        masked_msg[i] = msg[i] ^ mask_key[i % 4]

    s.sendall(header + masked_msg)

def ws_recv(s):
    header = s.recv(2)
    if not header:
        return None
    length = header[1] & 0x7F
    if length == 126:
        length = int.from_bytes(s.recv(2), 'big')
    elif length == 127:
        length = int.from_bytes(s.recv(8), 'big')

    data = b""
    while len(data) < length:
        chunk = s.recv(length - len(data))
        if not chunk:
            break
        data += chunk
    return data.decode('utf-8')

def test_websocket_server():
    test_file = "/tmp/test_target.txt"
    test_content = "Hello, World!\n"
    with open(test_file, "w") as f:
        f.write(test_content)

    file_size = len(test_content)

    # 1. Connect
    s = ws_connect("127.0.0.1", 9050, "/analyze")

    # 2. Valid request
    req1 = json.dumps({"target_file": test_file})
    ws_send(s, req1)
    resp1 = ws_recv(s)

    expected_prefix = f"ANALYSIS_RESULT:{file_size}_OK"
    assert resp1 is not None, "No response received for valid request"
    assert resp1.strip() == expected_prefix, f"Expected response starting with {expected_prefix}, got {resp1}"

    # 3. Invalid JSON
    ws_send(s, '{"bad": "data"}')
    resp2 = ws_recv(s)
    assert resp2 is not None, "No response received for invalid JSON"
    assert resp2.strip() == "ERROR", f"Expected ERROR for invalid JSON, got {resp2}"

    # 4. Non-existent file
    req3 = json.dumps({"target_file": "/tmp/does_not_exist_12345.txt"})
    ws_send(s, req3)
    resp3 = ws_recv(s)
    assert resp3 is not None, "No response received for non-existent file"
    assert resp3.strip() == "ERROR", f"Expected ERROR for non-existent file, got {resp3}"

    s.close()