# test_final_state.py

import os
import socket
import base64
import hashlib
import struct
import pytest

def test_server_pid_exists():
    pid_file = "/home/user/server.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"

    pid = int(pid_str)
    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

def test_libexpr_built():
    so_file = "/home/user/libexpr/build/libexpr.so"
    assert os.path.isfile(so_file), f"Shared library {so_file} was not built or is in the wrong location."

def test_rust_project_exists():
    assert os.path.isdir("/home/user/ws_eval"), "Rust project directory /home/user/ws_eval is missing."
    assert os.path.isfile("/home/user/ws_eval/Cargo.toml"), "Cargo.toml is missing in the Rust project."
    assert os.path.isfile("/home/user/ws_eval/build.rs"), "build.rs is missing in the Rust project."

def ws_send_recv(host, port, message):
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
        f"Sec-WebSocket-Version: 13\r\n"
        f"\r\n"
    )
    s.sendall(handshake.encode('utf-8'))
    resp = s.recv(4096)
    if b"101 Switching Protocols" not in resp:
        s.close()
        raise Exception("WebSocket handshake failed")

    msg_bytes = message.encode('utf-8')
    length = len(msg_bytes)
    header = bytearray([0x81])
    header.append(0x80 | length)
    mask = os.urandom(4)
    header.extend(mask)

    masked_data = bytearray(length)
    for i in range(length):
        masked_data[i] = msg_bytes[i] ^ mask[i % 4]

    s.sendall(header + masked_data)

    header = s.recv(2)
    if not header:
        s.close()
        raise Exception("No response from WebSocket server")

    payload_len = header[1] & 0x7f
    if payload_len == 126:
        s.recv(2)
    elif payload_len == 127:
        s.recv(8)

    data = s.recv(payload_len)
    s.close()
    return data.decode('utf-8')

def test_websocket_addition():
    try:
        res = ws_send_recv("127.0.0.1", 9001, "ADD 15 25")
        assert res == "40", f"Expected '40' for 'ADD 15 25', got '{res}'"
    except Exception as e:
        pytest.fail(f"WebSocket test failed: {e}")

def test_websocket_subtraction():
    try:
        res = ws_send_recv("127.0.0.1", 9001, "SUB 100 42")
        assert res == "58", f"Expected '58' for 'SUB 100 42', got '{res}'"
    except Exception as e:
        pytest.fail(f"WebSocket test failed: {e}")

def test_websocket_buffer_overflow_safety():
    try:
        res = ws_send_recv("127.0.0.1", 9001, "THIS_IS_A_VERY_LONG_OPERATION_NAME_THAT_WOULD_CRASH_IT 10 20")
        assert res == "ERROR", f"Expected 'ERROR' for invalid/long operation, got '{res}'"
    except Exception as e:
        pytest.fail(f"WebSocket test failed (possibly crashed due to buffer overflow): {e}")