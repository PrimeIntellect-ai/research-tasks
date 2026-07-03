# test_final_state.py

import socket
import json
import os
import pytest

def test_websocket_server():
    """Test the WebSocket server for correct authentication and data transformation."""
    host = '127.0.0.1'
    port = 9001

    # 1. Test unauthorized connection
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect((host, port))
        req_unauth = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            f"Sec-WebSocket-Version: 13\r\n"
            f"\r\n"
        )
        s.sendall(req_unauth.encode('utf-8'))
        resp_unauth = s.recv(4096).decode('utf-8', errors='ignore')
        s.close()
        status_line = resp_unauth.split('\r\n')[0]
        assert "401" in status_line, f"Expected 401 Unauthorized for missing token, got: {status_line}"
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to {host}:{port}. Is the Rust service running?")

    # 2. Test authorized connection and data transformation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect((host, port))
    req_auth = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
        f"Sec-WebSocket-Version: 13\r\n"
        f"Authorization: Bearer secret-ci-token\r\n"
        f"\r\n"
    )
    s.sendall(req_auth.encode('utf-8'))
    resp_auth = s.recv(4096).decode('utf-8', errors='ignore')
    status_line = resp_auth.split('\r\n')[0]
    assert "101" in status_line, f"Expected 101 Switching Protocols for valid token, got: {status_line}"

    # Prepare JSON payload
    payload_obj = [
        {"timestamp_sec": 4, "event_msg": "Click checkout", "source": "puppeteer"},
        {"timestamp_sec": 26, "event_msg": "Database lock", "source": "db"}
    ]
    payload = json.dumps(payload_obj).encode('utf-8')

    # Construct WebSocket text frame (Opcode 1), masked
    frame = bytearray([0x81])
    if len(payload) < 126:
        frame.append(0x80 | len(payload))
    elif len(payload) < 65536:
        frame.append(0x80 | 126)
        frame.extend(len(payload).to_bytes(2, 'big'))
    else:
        frame.append(0x80 | 127)
        frame.extend(len(payload).to_bytes(8, 'big'))

    mask_key = os.urandom(4)
    frame.extend(mask_key)
    for i in range(len(payload)):
        frame.append(payload[i] ^ mask_key[i % 4])

    s.sendall(frame)

    # Receive WebSocket response frame
    resp_frame = b""
    while len(resp_frame) < 2:
        chunk = s.recv(4096)
        if not chunk:
            break
        resp_frame += chunk

    assert len(resp_frame) >= 2, "Did not receive a valid WebSocket response frame."

    opcode = resp_frame[0] & 0x0F
    assert opcode == 1, f"Expected text frame (opcode 1), got opcode {opcode}."

    payload_len = resp_frame[1] & 0x7F
    offset = 2
    if payload_len == 126:
        while len(resp_frame) < 4:
            resp_frame += s.recv(4096)
        payload_len = int.from_bytes(resp_frame[2:4], 'big')
        offset = 4
    elif payload_len == 127:
        while len(resp_frame) < 10:
            resp_frame += s.recv(4096)
        payload_len = int.from_bytes(resp_frame[2:10], 'big')
        offset = 10

    while len(resp_frame) < offset + payload_len:
        resp_frame += s.recv(4096)

    s.close()

    resp_data = resp_frame[offset:offset+payload_len].decode('utf-8')

    try:
        resp_json = json.loads(resp_data)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse response as JSON. Raw response: {resp_data}")

    expected = [
        {"timestamp_sec": 4, "event_msg": "Click checkout", "source": "puppeteer"},
        {"timestamp_sec": 4, "event_msg": "Visual Error Detected", "source": "ui_test"},
        {"timestamp_sec": 15, "event_msg": "Visual Error Detected", "source": "ui_test"},
        {"timestamp_sec": 26, "event_msg": "Database lock", "source": "db"},
        {"timestamp_sec": 27, "event_msg": "Visual Error Detected", "source": "ui_test"}
    ]

    assert resp_json == expected, f"Response JSON does not match expected output.\nExpected: {expected}\nGot: {resp_json}"