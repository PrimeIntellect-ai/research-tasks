# test_final_state.py

import os
import json
import socket
import base64
import time
import pytest

CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def send_ws_message(port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(('localhost', port))
        key = base64.b64encode(os.urandom(16)).decode('utf-8')
        request = (
            f"GET / HTTP/1.1\r\n"
            f"Host: localhost:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        s.sendall(request.encode())
        resp = s.recv(4096)
        if b"101 Switching Protocols" not in resp:
            raise Exception("WebSocket handshake failed")

        msg_bytes = message.encode('utf-8')
        length = len(msg_bytes)
        frame = bytearray([0x81])
        if length < 126:
            frame.append(length | 0x80)
        elif length < 65536:
            frame.append(126 | 0x80)
            frame.extend(length.to_bytes(2, 'big'))
        else:
            frame.append(127 | 0x80)
            frame.extend(length.to_bytes(8, 'big'))

        mask = os.urandom(4)
        frame.extend(mask)
        for i in range(length):
            frame.append(msg_bytes[i] ^ mask[i % 4])

        s.sendall(frame)
    finally:
        s.close()

def redis_command(cmd_args):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(('localhost', 6379))
        req = f"*{len(cmd_args)}\r\n"
        for arg in cmd_args:
            arg_bytes = str(arg).encode('utf-8')
            req += f"${len(arg_bytes)}\r\n{arg}\r\n"
        s.sendall(req.encode('utf-8'))
        resp = s.recv(8192)
        return resp
    finally:
        s.close()

def test_environment_ready():
    assert os.path.exists("/home/user/environment_ready.log"), "The /home/user/environment_ready.log file is missing."
    with open("/home/user/environment_ready.log", "r") as f:
        assert "READY" in f.read(), "The environment_ready.log does not contain 'READY'."

def test_services_running():
    # Check Redis
    try:
        resp = redis_command(["PING"])
        assert b"PONG" in resp, "Redis is not responding properly."
    except Exception as e:
        pytest.fail(f"Redis is not running on port 6379: {e}")

    # Check Backend
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', 5000))
    except Exception as e:
        pytest.fail(f"Python backend is not running on port 5000: {e}")
    finally:
        s.close()

    # Check Rust Proxy
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', 8080))
    except Exception as e:
        pytest.fail(f"Rust Proxy is not running on port 8080: {e}")
    finally:
        s.close()

def test_adversarial_corpus():
    redis_command(["FLUSHALL"])

    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean payloads found."
    assert len(evil_files) > 0, "No evil payloads found."

    for cf in clean_files:
        with open(os.path.join(CLEAN_DIR, cf), 'r') as f:
            payload = f.read()
        send_ws_message(8080, payload)

    for ef in evil_files:
        with open(os.path.join(EVIL_DIR, ef), 'r') as f:
            payload = f.read()
        send_ws_message(8080, payload)

    time.sleep(2) # Wait for ingestion

    db_size_resp = redis_command(["DBSIZE"])
    # Parse Redis integer response: :<number>\r\n
    try:
        size_str = db_size_resp.split(b'\r\n')[0]
        assert size_str.startswith(b':')
        db_size = int(size_str[1:])
    except Exception as e:
        pytest.fail(f"Failed to parse DBSIZE from Redis: {db_size_resp}")

    if db_size != len(clean_files):
        pytest.fail(f"Expected {len(clean_files)} clean entries in Redis, but found {db_size}. "
                    f"This means either clean payloads were dropped or evil payloads were accepted.")