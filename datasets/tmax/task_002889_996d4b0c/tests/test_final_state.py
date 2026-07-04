# test_final_state.py

import socket
import base64
import os
import json
import time
import pytest

def ws_connect(host, port, path, headers=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect((host, port))
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Version: 13\r\nSec-WebSocket-Key: {key}\r\n"
    if headers:
        for k, v in headers.items():
            req += f"{k}: {v}\r\n"
    req += "\r\n"
    s.sendall(req.encode('utf-8'))
    resp = s.recv(4096)
    return s, resp

def ws_send_text(s, text):
    payload = text.encode('utf-8')
    header = bytearray([0x81]) # FIN + Text Frame
    mask_key = os.urandom(4)
    length = len(payload)
    if length < 126:
        header.append(length | 0x80)
    elif length < 65536:
        header.append(126 | 0x80)
        header.extend(length.to_bytes(2, 'big'))
    else:
        header.append(127 | 0x80)
        header.extend(length.to_bytes(8, 'big'))
    header.extend(mask_key)
    masked_payload = bytearray(length)
    for i in range(length):
        masked_payload[i] = payload[i] ^ mask_key[i % 4]
    s.sendall(header + masked_payload)

def ws_recv_text(s):
    header = s.recv(2)
    if not header:
        return None
    b1, b2 = header[0], header[1]
    opcode = b1 & 0x0f
    masked = (b2 & 0x80) != 0
    length = b2 & 0x7f
    if length == 126:
        length = int.from_bytes(s.recv(2), 'big')
    elif length == 127:
        length = int.from_bytes(s.recv(8), 'big')
    if masked:
        mask_key = s.recv(4)
    payload = b""
    while len(payload) < length:
        chunk = s.recv(length - len(payload))
        if not chunk:
            break
        payload += chunk
    if masked:
        unmasked = bytearray(length)
        for i in range(length):
            unmasked[i] = payload[i] ^ mask_key[i % 4]
        payload = unmasked
    if opcode == 1:
        return payload.decode('utf-8')
    return None

def test_websocket_server_unauthorized():
    """Ensure that the server rejects unauthenticated requests."""
    s, resp = ws_connect("127.0.0.1", 8080, "/ws/device_99")
    s.close()
    resp_str = resp.decode('utf-8', errors='ignore')
    assert "401" in resp_str.split("\r\n")[0], f"Expected HTTP 401 Unauthorized, got: {resp_str.split(chr(13))[0]}"

def test_websocket_server_authorized_and_payloads():
    """Ensure the server accepts authenticated requests, processes hex code, and returns correct counts."""
    headers = {"Authorization": "Bearer TKN_A93F8B2C"}
    s, resp = ws_connect("127.0.0.1", 8080, "/ws/device_99", headers)
    resp_str = resp.decode('utf-8', errors='ignore')
    assert "101" in resp_str.split("\r\n")[0], f"Expected HTTP 101 Switching Protocols, got: {resp_str.split(chr(13))[0]}"

    # Test 1: Two mov instructions
    payload1 = {"id": "test_1", "hex_code": "48c7c00100000048c7c302000000"}
    ws_send_text(s, json.dumps(payload1))
    resp1_text = ws_recv_text(s)
    assert resp1_text is not None, "Did not receive response for test_1"
    resp1 = json.loads(resp1_text)
    assert resp1.get("id") == "test_1", f"Expected id 'test_1', got {resp1.get('id')}"
    assert resp1.get("mov_count") == 2, f"Expected mov_count 2, got {resp1.get('mov_count')}"

    # Test 2: Zero mov instructions
    payload2 = {"id": "test_2", "hex_code": "909090"}
    ws_send_text(s, json.dumps(payload2))
    resp2_text = ws_recv_text(s)
    assert resp2_text is not None, "Did not receive response for test_2"
    resp2 = json.loads(resp2_text)
    assert resp2.get("id") == "test_2", f"Expected id 'test_2', got {resp2.get('id')}"
    assert resp2.get("mov_count") == 0, f"Expected mov_count 0, got {resp2.get('mov_count')}"

    s.close()

def test_telemetry_log_contents():
    """Ensure that the telemetry log is correctly appended with processed messages."""
    time.sleep(1) # Allow time for async logging
    log_path = "/app/telemetry.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # We expect at least the two lines we just generated
    found_test_1 = False
    found_test_2 = False

    for line in lines:
        try:
            entry = json.loads(line)
            if entry.get("device_id") == "device_99" and entry.get("msg_id") == "test_1" and entry.get("mov_count") == 2:
                found_test_1 = True
            if entry.get("device_id") == "device_99" and entry.get("msg_id") == "test_2" and entry.get("mov_count") == 0:
                found_test_2 = True
        except json.JSONDecodeError:
            continue

    assert found_test_1, "Log entry for test_1 not found or incorrect in /app/telemetry.log"
    assert found_test_2, "Log entry for test_2 not found or incorrect in /app/telemetry.log"