# test_final_state.py

import os
import socket
import base64
import hashlib
import subprocess
import time
import pytest

def test_nginx_running():
    """Test that Nginx is running and listening on port 8080."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "nginx"], text=True)
        assert output.strip() != "", "Nginx is not running."
    except subprocess.CalledProcessError:
        pytest.fail("Nginx is not running.")

def test_server_running_under_valgrind():
    """Test that divn_server is running under valgrind."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "valgrind.*divn_server"], text=True)
        assert output.strip() != "", "divn_server is not running under valgrind."
    except subprocess.CalledProcessError:
        pytest.fail("divn_server is not running under valgrind.")

def test_websocket_fletcher16_and_memory_leak():
    """Test the websocket proxy, Fletcher-16 calculation, and memory leak fix."""
    # 1. Connect via websocket and test the checksum
    payload = b"hello world"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(('127.0.0.1', 8080))
    except Exception as e:
        pytest.fail(f"Could not connect to Nginx on port 8080: {e}")

    # WebSocket Handshake
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    req = (
        "GET / HTTP/1.1\r\n"
        "Host: 127.0.0.1:8080\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode())

    try:
        handshake_resp = s.recv(4096)
        assert b"101 Switching Protocols" in handshake_resp, "WebSocket handshake failed. Is Nginx proxying headers correctly?"
    except Exception as e:
        pytest.fail(f"Failed to receive handshake response: {e}")

    # Send Binary Frame
    # FIN + Opcode 2 (Binary) = 0x82
    mask_key = os.urandom(4)
    frame = bytearray([0x82, 0x80 | len(payload)])
    frame.extend(mask_key)
    for i in range(len(payload)):
        frame.append(payload[i] ^ mask_key[i % 4])

    s.sendall(frame)

    try:
        resp_frame = s.recv(4096)
    except Exception as e:
        pytest.fail(f"Failed to receive websocket frame: {e}")
    finally:
        s.close()

    assert len(resp_frame) >= 2, "Received empty or invalid websocket frame."

    payload_len = resp_frame[1] & 0x7F
    if payload_len < 126:
        data = resp_frame[2:2+payload_len]
    elif payload_len == 126:
        data = resp_frame[4:4+(resp_frame[2]<<8 | resp_frame[3])]
    else:
        data = resp_frame[10:] # Simplified for this test

    # The Fletcher-16 for "hello world" is 0x4642 (or 17986).
    # The C server might return it as a string or raw bytes depending on implementation, 
    # but the prompt says "matches the expected checksum string/bytes".
    # We will check if "4642" or the integer string is in the response.
    resp_str = data.decode('utf-8', errors='ignore').lower()
    resp_hex = data.hex().lower()

    assert "4642" in resp_str or "4642" in resp_hex or "17986" in resp_str, \
        f"Fletcher-16 checksum incorrect or not found in response. Got: {data}"

    # 2. Shutdown server gracefully to flush valgrind logs
    subprocess.run(["pkill", "-INT", "-f", "divn_server"])

    # Wait for valgrind to write logs and exit
    for _ in range(10):
        time.sleep(0.5)
        if subprocess.run(["pgrep", "-f", "valgrind.*divn_server"]).returncode != 0:
            break

    # 3. Check valgrind log for memory leaks
    valgrind_log_path = "/home/user/valgrind.log"
    assert os.path.exists(valgrind_log_path), f"{valgrind_log_path} does not exist."

    with open(valgrind_log_path, "r") as f:
        log_content = f.read()

    leak_free = "definitely lost: 0 bytes in 0 blocks" in log_content or \
                "All heap blocks were freed -- no leaks are possible" in log_content

    assert leak_free, "Memory leak detected in valgrind.log. Ensure you freed the allocated buffer."