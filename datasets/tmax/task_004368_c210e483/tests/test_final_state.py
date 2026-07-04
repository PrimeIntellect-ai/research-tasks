# test_final_state.py
import os
import socket
import subprocess
import time
import pytest

HOST = '127.0.0.1'
PORT = 9000
TOKEN = 'X9K2-M4RQ-77AA'

def get_server_pid():
    try:
        # Try using ss
        out = subprocess.check_output(["ss", "-lptn", f"sport = :{PORT}"], text=True)
        for line in out.splitlines():
            if str(PORT) in line and "pid=" in line:
                parts = line.split("pid=")
                pid_str = parts[1].split(",")[0]
                return int(pid_str)
    except Exception:
        pass

    try:
        # Try using lsof
        out = subprocess.check_output(["lsof", "-t", "-i", f":{PORT}"], text=True)
        return int(out.strip().split()[0])
    except Exception:
        pass

    return None

def get_memory_usage(pid):
    try:
        with open(f"/proc/{pid}/statm", "r") as f:
            # second value is resident set size in pages
            rss_pages = int(f.read().split()[1])
            return rss_pages * 4096
    except Exception:
        return 0

def send_request(sock, request_bytes):
    sock.sendall(request_bytes)
    return sock.recv(1024)

@pytest.fixture(scope="module")
def server_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((HOST, PORT))
        yield s
    finally:
        s.close()

def test_valid_request(server_connection):
    req = f"AUTH {TOKEN}|DATA Hello World\n".encode('utf-8')
    resp = send_request(server_connection, req)
    assert resp == b"OK\n", f"Expected OK\\n, got {resp!r}"

def test_invalid_token(server_connection):
    req = b"AUTH WRONG|DATA Hello\n"
    resp = send_request(server_connection, req)
    assert resp == b"AUTH_FAIL\n", f"Expected AUTH_FAIL\\n, got {resp!r}"

def test_corrupted_payload(server_connection):
    # Corrupted payload from the pcap description
    req = f"AUTH {TOKEN}|DATA \x00\xff\xff\xff\xff\n".encode('latin1')
    resp = send_request(server_connection, req)
    assert resp == b"ERROR\n", f"Expected ERROR\\n for corrupted payload, got {resp!r}"

    # Connection should still be alive
    req2 = f"AUTH {TOKEN}|DATA Hello Again\n".encode('utf-8')
    resp2 = send_request(server_connection, req2)
    assert resp2 == b"OK\n", f"Expected OK\\n after corrupted payload, got {resp2!r}"

def test_memory_leak():
    pid = get_server_pid()
    assert pid is not None, f"Could not find process listening on {PORT}"

    initial_mem = get_memory_usage(pid)
    assert initial_mem > 0, "Could not read initial memory usage"

    # Send 10,000 valid requests to check for memory leaks
    # (Reduced from 50k to 10k to ensure tests run reasonably fast while still catching 10MB+ leaks)
    req = f"AUTH {TOKEN}|DATA Memory Test Payload\n".encode('utf-8')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10.0)
    s.connect((HOST, PORT))

    for _ in range(10000):
        s.sendall(req)
        resp = s.recv(1024)
        if resp != b"OK\n":
            pytest.fail(f"Server stopped responding correctly during load test: {resp!r}")

    s.close()

    final_mem = get_memory_usage(pid)

    # If 1024 bytes are leaked per request, 10,000 requests = ~10MB
    # We allow a small growth (e.g., 2MB) for normal buffering
    mem_diff = final_mem - initial_mem
    assert mem_diff < 2 * 1024 * 1024, f"Memory leak detected: usage grew by {mem_diff} bytes"