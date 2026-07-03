# test_final_state.py
import os
import socket
import hashlib
import base64
import time
import pytest

PASSPHRASE = "hunter two security"
HOST = "127.0.0.1"
PORT = 8080

def send_request(filename, payload_bytes, passphrase, override_hash=None):
    payload_b64 = base64.b64encode(payload_bytes).decode('utf-8')
    if override_hash:
        hash_hex = override_hash
    else:
        m = hashlib.sha256()
        m.update(payload_bytes)
        m.update(passphrase.encode('utf-8'))
        hash_hex = m.hexdigest()

    req = f"FILENAME {filename}\nHASH {hash_hex}\nPAYLOAD {payload_b64}\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((HOST, PORT))
        s.sendall(req.encode('utf-8'))
        resp = s.recv(1024).decode('utf-8')
        return resp

def test_valid_request():
    payload = b"hello world"
    filename = "valid.txt"
    resp = send_request(filename, payload, PASSPHRASE)
    assert resp == "OK\n", f"Expected OK\\n for valid request, got: {repr(resp)}"

    filepath = f"/home/user/uploads/{filename}"
    assert os.path.isfile(filepath), f"File {filepath} was not created."
    with open(filepath, "rb") as f:
        assert f.read() == payload, f"File {filepath} content mismatch."

def test_path_traversal():
    payload = b"evil payload"
    filename = "../hacked.txt"
    resp = send_request(filename, payload, PASSPHRASE)
    assert resp == "ERROR\n", f"Expected ERROR\\n for path traversal, got: {repr(resp)}"

    filepath = "/home/user/hacked.txt"
    assert not os.path.exists(filepath), f"Path traversal succeeded, {filepath} was created."

def test_invalid_hash():
    payload = b"bad hash payload"
    filename = "badhash.txt"
    resp = send_request(filename, payload, PASSPHRASE, override_hash="badhash"*8)
    assert resp == "ERROR\n", f"Expected ERROR\\n for invalid hash, got: {repr(resp)}"

    filepath = f"/home/user/uploads/{filename}"
    assert not os.path.exists(filepath), f"File {filepath} was created despite invalid hash."

def test_server_log():
    log_path = "/home/user/server.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read()

    # It should contain exactly "Written: valid.txt" from our valid request.
    # We only assert that it is in the log, as there might be other valid requests if the tests run multiple times.
    assert "Written: valid.txt" in content, f"Log file does not contain expected entry. Content: {content}"