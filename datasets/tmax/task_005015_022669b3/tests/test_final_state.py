# test_final_state.py

import socket
import requests
import pytest

def test_unauthorized_requests():
    """Test that requests without the correct Authorization header are rejected."""
    url = "http://127.0.0.1:8080/api/waf"

    # Missing auth header
    try:
        r1 = requests.get(url, timeout=2)
        assert r1.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {r1.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

    # Incorrect auth header
    headers = {"Authorization": "Bearer INVALID-TOKEN"}
    r2 = requests.get(url, headers=headers, timeout=2)
    assert r2.status_code in (401, 403), f"Expected 401 or 403 for invalid auth, got {r2.status_code}"

def test_websocket_flow():
    """Test the complete WebSocket upgrade and WAF engine processing flow."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(("127.0.0.1", 8080))
    except Exception as e:
        pytest.fail(f"Could not connect to 127.0.0.1:8080: {e}")

    # HTTP Upgrade request
    req = (
        "GET /api/waf HTTP/1.1\r\n"
        "Host: 127.0.0.1:8080\r\n"
        "Connection: Upgrade\r\n"
        "Upgrade: websocket\r\n"
        "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "Authorization: Bearer WAF-2024-SEC\r\n\r\n"
    )
    s.sendall(req.encode('utf-8'))

    # Read HTTP response
    resp = s.recv(4096)
    assert b"101 Switching Protocols" in resp, f"Failed to upgrade to WebSocket. Response: {resp}"

    # Construct a masked WebSocket text frame
    payload = b"<script>alert(1)</script>\n"
    frame = bytearray()
    frame.append(0x81) # FIN bit set, Opcode 1 (Text)
    frame.append(0x80 | len(payload)) # Mask bit set, payload length

    mask = [0x12, 0x34, 0x56, 0x78]
    frame.extend(mask)

    for i, b in enumerate(payload):
        frame.append(b ^ mask[i % 4])

    s.sendall(frame)

    # Read WebSocket response frame
    try:
        resp_frame = s.recv(4096)
    except socket.timeout:
        pytest.fail("Timed out waiting for WebSocket response from the WAF engine.")

    assert len(resp_frame) >= 2, "Received invalid or empty WebSocket response."

    # Server-to-client frames are not masked
    assert resp_frame[0] == 0x81, f"Expected Text frame (0x81), got {hex(resp_frame[0])}"

    payload_len = resp_frame[1] & 0x7F
    offset = 2
    if payload_len == 126:
        payload_len = int.from_bytes(resp_frame[2:4], 'big')
        offset = 4
    elif payload_len == 127:
        payload_len = int.from_bytes(resp_frame[2:10], 'big')
        offset = 10

    actual_payload = resp_frame[offset:offset+payload_len]
    expected_payload = b"[WAF-SECURE] <script>alert(1)</script>\n"

    assert actual_payload == expected_payload, f"WAF engine output mismatch.\nExpected: {expected_payload}\nGot: {actual_payload}"

    s.close()