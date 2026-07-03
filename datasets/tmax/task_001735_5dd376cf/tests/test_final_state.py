# test_final_state.py

import os
import subprocess
import socket
import base64
import struct
import pytest

def test_files_exist():
    cpp_file = "/home/user/ws_firewall.cpp"
    bin_file = "/home/user/ws_firewall_bin"
    bench_file = "/home/user/bench_results.txt"

    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."
    assert os.path.isfile(bin_file), f"Compiled binary {bin_file} is missing."
    assert os.path.isfile(bench_file), f"Benchmark results {bench_file} is missing."

    with open(bench_file, "r") as f:
        content = f.read().strip()
    assert len(content) > 0, f"Benchmark results file {bench_file} is empty."

def test_static_binary():
    bin_file = "/home/user/ws_firewall_bin"
    result = subprocess.run(["file", bin_file], capture_output=True, text=True)
    assert "statically linked" in result.stdout.lower(), f"Binary {bin_file} is not statically linked. 'file' output: {result.stdout}"

def ws_send_recv(host, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((host, port))

        key = base64.b64encode(os.urandom(16)).decode('utf-8')
        req = f"GET / HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        s.sendall(req.encode('utf-8'))

        resp = s.recv(4096)
        if b"101 Switching Protocols" not in resp:
            s.close()
            raise Exception("WebSocket handshake failed")

        msg_bytes = message.encode('utf-8')
        length = len(msg_bytes)
        header = bytearray([0x81])
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack(">H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack(">Q", length))

        mask = os.urandom(4)
        header.extend(mask)
        masked_data = bytearray(length)
        for i in range(length):
            masked_data[i] = msg_bytes[i] ^ mask[i % 4]
        s.sendall(header + masked_data)

        header_recv = s.recv(2)
        if not header_recv:
            s.close()
            return ""
        b1, b2 = header_recv[0], header_recv[1]
        payload_len = b2 & 0x7F
        if payload_len == 126:
            ext = s.recv(2)
            payload_len = struct.unpack(">H", ext)[0]
        elif payload_len == 127:
            ext = s.recv(8)
            payload_len = struct.unpack(">Q", ext)[0]

        data = b""
        while len(data) < payload_len:
            chunk = s.recv(payload_len - len(data))
            if not chunk:
                break
            data += chunk
        return data.decode('utf-8', errors='ignore')
    finally:
        s.close()

def test_adversarial_corpus():
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        with open(os.path.join(evil_dir, f), "r") as file:
            content = file.read()
        try:
            resp = ws_send_recv("127.0.0.1", 8080, content)
            if resp != "REJECT":
                evil_bypassed.append(f)
        except Exception as e:
            evil_bypassed.append(f"{f} (Error: {str(e)})")

    for f in clean_files:
        with open(os.path.join(clean_dir, f), "r") as file:
            content = file.read()
        try:
            resp = ws_send_recv("127.0.0.1", 8080, content)
            if resp != "ACK":
                clean_modified.append(f)
        except Exception as e:
            clean_modified.append(f"{f} (Error: {str(e)})")

    error_msg = ""
    if evil_bypassed:
        error_msg += f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}. "
    if clean_modified:
        error_msg += f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}."

    assert not evil_bypassed and not clean_modified, error_msg.strip()