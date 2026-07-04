# test_final_state.py

import os
import json
import socket
import base64
import hashlib
import subprocess
import time
import pytest

def test_done_file():
    done_path = "/home/user/done.txt"
    assert os.path.exists(done_path), f"Missing {done_path}"
    with open(done_path, "r") as f:
        content = f.read().strip()
    assert content == "READY", f"Expected 'READY' in {done_path}, got '{content}'"

def test_rust_compiled():
    so_path = "/home/user/rust_hasher/target/release/librust_hasher.so"
    assert os.path.exists(so_path), f"Missing compiled Rust library at {so_path}"

def test_server_script_exists():
    script_path = "/home/user/artifact_server.py"
    assert os.path.exists(script_path), f"Missing Python script at {script_path}"

def ws_connect_and_send(port, messages):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect(('localhost', port))

    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    handshake = (
        f"GET / HTTP/1.1\r\n"
        f"Host: localhost:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(handshake.encode('utf-8'))
    resp = s.recv(4096)
    if b"101 Switching Protocols" not in resp:
        raise Exception("WebSocket Handshake failed")

    results = []
    for msg in messages:
        payload = json.dumps(msg).encode('utf-8')
        frame = bytearray([0x81]) # FIN + Text

        mask_key = os.urandom(4)
        if len(payload) < 126:
            frame.append(len(payload) | 0x80)
        elif len(payload) < 65536:
            frame.append(126 | 0x80)
            frame.extend(len(payload).to_bytes(2, 'big'))
        else:
            frame.append(127 | 0x80)
            frame.extend(len(payload).to_bytes(8, 'big'))

        frame.extend(mask_key)
        for i in range(len(payload)):
            frame.append(payload[i] ^ mask_key[i % 4])

        s.sendall(frame)

        header = s.recv(2)
        if not header:
            break
        opcode = header[0] & 0x0f
        payload_len = header[1] & 0x7f
        if payload_len == 126:
            payload_len = int.from_bytes(s.recv(2), 'big')
        elif payload_len == 127:
            payload_len = int.from_bytes(s.recv(8), 'big')

        data = b""
        while len(data) < payload_len:
            data += s.recv(payload_len - len(data))

        results.append(json.loads(data.decode('utf-8')))

    s.close()
    return results

def test_websocket_server_logic():
    # Setup test files
    test_dir = "/home/user/artifacts_test"
    os.makedirs(test_dir, exist_ok=True)

    file1 = os.path.join(test_dir, "test1.txt")
    file2 = os.path.join(test_dir, "test2.txt")
    file3 = os.path.join(test_dir, "test3.txt")

    with open(file1, "w") as f: f.write("Data1")
    with open(file2, "w") as f: f.write("Data2")
    with open(file3, "w") as f: f.write("Data3")

    # Start the server if not already running, or just run it to be sure
    proc = subprocess.Popen(["python3", "/home/user/artifact_server.py"])

    try:
        # Wait for server to start
        time.sleep(2)

        req1 = {
            "id": "build-1",
            "files": [file1, file2]
        }

        req2 = {
            "id": "build-2",
            "files": [file2, file3]
        }

        # Before req2, modify file2
        def modify_file():
            with open(file2, "w") as f: f.write("Data2_Modified")

        # We will send req1, then modify file2, then send req2.
        # Since our ws_connect_and_send sends all at once, we need to split it or just do it in inline steps.

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect(('localhost', 8765))

        key = base64.b64encode(os.urandom(16)).decode('utf-8')
        handshake = (
            f"GET / HTTP/1.1\r\n"
            f"Host: localhost:8765\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        s.sendall(handshake.encode('utf-8'))
        resp = s.recv(4096)
        assert b"101 Switching Protocols" in resp, "Server did not accept WS handshake"

        def send_msg(msg):
            payload = json.dumps(msg).encode('utf-8')
            frame = bytearray([0x81])
            mask_key = os.urandom(4)
            if len(payload) < 126:
                frame.append(len(payload) | 0x80)
            elif len(payload) < 65536:
                frame.append(126 | 0x80)
                frame.extend(len(payload).to_bytes(2, 'big'))
            else:
                frame.append(127 | 0x80)
                frame.extend(len(payload).to_bytes(8, 'big'))
            frame.extend(mask_key)
            for i in range(len(payload)):
                frame.append(payload[i] ^ mask_key[i % 4])
            s.sendall(frame)

        def recv_msg():
            header = s.recv(2)
            payload_len = header[1] & 0x7f
            if payload_len == 126:
                payload_len = int.from_bytes(s.recv(2), 'big')
            elif payload_len == 127:
                payload_len = int.from_bytes(s.recv(8), 'big')
            data = b""
            while len(data) < payload_len:
                data += s.recv(payload_len - len(data))
            return json.loads(data.decode('utf-8'))

        send_msg(req1)
        res1 = recv_msg()

        assert res1["id"] == "build-1"
        assert len(res1["sorted_hashes"]) == 2
        assert len(res1["diff"]["added"]) == 2
        assert res1["sorted_hashes"][0]["file"] == file1
        assert res1["sorted_hashes"][1]["file"] == file2

        modify_file()

        send_msg(req2)
        res2 = recv_msg()

        assert res2["id"] == "build-2"
        assert file3 in res2["diff"]["added"], "file3 should be added"
        assert file1 in res2["diff"]["removed"], "file1 should be removed"
        assert file2 in res2["diff"]["modified"], "file2 should be modified"

        s.close()

    finally:
        proc.terminate()
        proc.wait()