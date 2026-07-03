# test_final_state.py

import os
import socket
import base64
import secrets
import struct
import subprocess
import requests
import pytest

def test_ready_file():
    ready_path = "/home/user/app/ready.txt"
    assert os.path.isfile(ready_path), f"{ready_path} is missing"
    with open(ready_path, 'r') as f:
        content = f.read().strip()
    assert content == "DONE", f"Expected 'DONE' in ready.txt, got '{content}'"

def test_go_tests_pass():
    chat_dir = "/home/user/app/chat-server"
    assert os.path.isdir(chat_dir), f"{chat_dir} is missing"

    result = subprocess.run(
        ["go", "test", "-v"],
        cwd=chat_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Go tests failed:\n{result.stdout}\n{result.stderr}"
    assert "testing/quick" in result.stdout or "testing/quick" in open(os.path.join(chat_dir, "router_test.go")).read(), "testing/quick not found in tests"

def test_test_results_log():
    log_path = "/home/user/app/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} is missing"
    with open(log_path, 'r') as f:
        content = f.read()
    assert len(content.strip()) > 0, "test_results.log is empty"

def ws_connect_and_send(host, port, path, token, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((host, port))
    except Exception as e:
        return f"Connection failed: {e}"

    key = base64.b64encode(secrets.token_bytes(16)).decode('utf-8')

    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n"
    )
    if token:
        request += f"Authorization: Bearer {token}\r\n"
    request += "\r\n"

    sock.sendall(request.encode('utf-8'))

    response = b""
    while b"\r\n\r\n" not in response:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

    headers, _, _ = response.partition(b"\r\n\r\n")
    if b"101 Switching Protocols" not in headers:
        sock.close()
        return headers.decode('utf-8', errors='ignore')

    # Send a masked text frame
    msg_bytes = message.encode('utf-8')
    frame = bytearray([0x81, 0x80 | len(msg_bytes)])
    masking_key = os.urandom(4)
    frame.extend(masking_key)
    for i in range(len(msg_bytes)):
        frame.append(msg_bytes[i] ^ masking_key[i % 4])

    sock.sendall(frame)

    # Read response frame
    try:
        resp_header = sock.recv(2)
        if len(resp_header) < 2:
            return "Connection closed without response"

        payload_len = resp_header[1] & 0x7F
        if payload_len == 126:
            ext_len = sock.recv(2)
            payload_len = struct.unpack(">H", ext_len)[0]
        elif payload_len == 127:
            ext_len = sock.recv(8)
            payload_len = struct.unpack(">Q", ext_len)[0]

        payload = sock.recv(payload_len)
        sock.close()
        return payload.decode('utf-8')
    except Exception as e:
        return f"Error reading response: {e}"

def test_websocket_echo_and_nginx_proxy():
    room_id = "abc12"
    message = "Hello World"
    expected_response = f"Room {room_id}: {message}"

    response = ws_connect_and_send(
        "127.0.0.1", 8080, f"/ws/room/{room_id}", 
        "secret-chat-token-123", message
    )

    assert response == expected_response, f"Expected WebSocket echo '{expected_response}', got '{response}'"

def test_websocket_unauthorized():
    headers = {
        "Connection": "Upgrade",
        "Upgrade": "websocket"
    }
    # No auth token
    resp = requests.get("http://127.0.0.1:8080/ws/room/abc12", headers=headers)
    assert resp.status_code == 401, f"Expected 401 Unauthorized for missing token, got {resp.status_code}"

    # Invalid auth token
    headers["Authorization"] = "Bearer wrong-token"
    resp = requests.get("http://127.0.0.1:8080/ws/room/abc12", headers=headers)
    assert resp.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {resp.status_code}"

def test_services_running():
    # Redis
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 6379))
    sock.close()
    assert result == 0, "Redis is not running on 127.0.0.1:6379"

    # Go Service
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 9000))
    sock.close()
    assert result == 0, "Go service is not running on 127.0.0.1:9000"

    # Nginx
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8080))
    sock.close()
    assert result == 0, "Nginx is not running on 127.0.0.1:8080"