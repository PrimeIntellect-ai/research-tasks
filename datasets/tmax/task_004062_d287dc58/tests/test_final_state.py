# test_final_state.py
import pytest
import json
import socket
import base64
import os

def get_websocket_data(host, port, path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10.0)
    try:
        s.connect((host, port))
    except Exception as e:
        pytest.fail(f"Could not connect to server at {host}:{port}. Is the server running? Error: {e}")

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

    resp = b""
    while b"\r\n\r\n" not in resp:
        chunk = s.recv(1024)
        if not chunk:
            pytest.fail("Connection closed before handshake completed.")
        resp += chunk

    if b"101 Switching Protocols" not in resp:
        pytest.fail(f"WebSocket handshake failed. Response header: {resp[:200]}")

    # Read WebSocket frame
    frame_head = s.recv(2)
    if not frame_head:
        pytest.fail("No data received from WebSocket after handshake.")

    payload_len = frame_head[1] & 0x7F
    if payload_len == 126:
        ext = s.recv(2)
        payload_len = int.from_bytes(ext, 'big')
    elif payload_len == 127:
        ext = s.recv(8)
        payload_len = int.from_bytes(ext, 'big')

    payload = b""
    while len(payload) < payload_len:
        chunk = s.recv(payload_len - len(payload))
        if not chunk:
            break
        payload += chunk

    s.close()
    return payload.decode('utf-8')

def test_websocket_accuracy():
    try:
        ws_response = get_websocket_data("127.0.0.1", 8080, "/ws")
    except Exception as e:
        pytest.fail(f"Failed to retrieve WebSocket data: {e}")

    try:
        data = json.loads(ws_response)
    except json.JSONDecodeError:
        pytest.fail(f"WebSocket response is not valid JSON: {ws_response[:100]}")

    truth = [
        {"state": 0, "start_frame": 0, "end_frame": 47},
        {"state": 1, "start_frame": 48, "end_frame": 119},
        {"state": 2, "start_frame": 120, "end_frame": 239}
    ]

    total_frames = 240

    truth_arr = [-1] * total_frames
    for t in truth:
        for i in range(t["start_frame"], min(t["end_frame"] + 1, total_frames)):
            truth_arr[i] = t["state"]

    pred_arr = [-1] * total_frames
    for p in data:
        start = p.get("start_frame")
        end = p.get("end_frame")
        state = p.get("state")
        if start is None or end is None or state is None:
            pytest.fail(f"Invalid JSON object format, missing keys: {p}")
        for i in range(start, min(end + 1, total_frames)):
            pred_arr[i] = state

    correct_frames = 0
    for i in range(total_frames):
        if truth_arr[i] == pred_arr[i] and truth_arr[i] != -1:
            correct_frames += 1

    accuracy = correct_frames / total_frames

    assert accuracy >= 0.95, f"Frame overlap accuracy is {accuracy:.4f}, which is below the 0.95 threshold."