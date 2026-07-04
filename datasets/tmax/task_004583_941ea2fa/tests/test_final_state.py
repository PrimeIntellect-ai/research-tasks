# test_final_state.py

import os
import socket
import ssl
import stat
import subprocess
import pytest

def generate_client_cert(cn, prefix):
    key_path = f"/tmp/{prefix}.key"
    csr_path = f"/tmp/{prefix}.csr"
    crt_path = f"/tmp/{prefix}.crt"

    subprocess.run([
        "openssl", "req", "-newkey", "rsa:2048", "-nodes",
        "-keyout", key_path, "-out", csr_path,
        "-subj", f"/CN={cn}"
    ], check=True, capture_output=True)

    subprocess.run([
        "openssl", "x509", "-req", "-in", csr_path,
        "-CA", "/app/certs/ca.crt", "-CAkey", "/app/certs/ca.key",
        "-CAcreateserial", "-out", crt_path, "-days", "1"
    ], check=True, capture_output=True)

    return crt_path, key_path

def test_no_client_cert():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="/app/certs/ca.crt")
    # Do not load client certificate
    try:
        with socket.create_connection(('127.0.0.1', 8443), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname='localhost') as ssock:
                ssock.sendall(b"ROTATE test AA000000000000E8\n")
                ssock.recv(1024)
        pytest.fail("Connection should have been rejected without a client certificate")
    except (ssl.SSLError, ConnectionResetError, socket.error):
        pass # Expected

def test_bad_cn():
    crt, key = generate_client_cert("Hacker", "bad")
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="/app/certs/ca.crt")
    context.load_cert_chain(certfile=crt, keyfile=key)

    try:
        with socket.create_connection(('127.0.0.1', 8443), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname='localhost') as ssock:
                ssock.sendall(b"ROTATE test AA000000000000E8\n")
                ssock.recv(1024)
        pytest.fail("Connection should have been rejected or dropped due to incorrect CN")
    except (ssl.SSLError, ConnectionResetError, socket.error):
        pass # Expected

def test_valid_admin_invalid_token():
    crt, key = generate_client_cert("Rotation-Admin", "admin_invalid")
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="/app/certs/ca.crt")
    context.load_cert_chain(certfile=crt, keyfile=key)

    with socket.create_connection(('127.0.0.1', 8443), timeout=2) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            # Token starts with AA, but XOR sum is not 0x42
            ssock.sendall(b"ROTATE db AA11223344556677\n")
            resp = ssock.recv(1024).decode()
            assert resp == "ERR INVALID_TOKEN\n", f"Expected ERR INVALID_TOKEN\\n, got: {repr(resp)}"

def test_valid_admin_valid_token():
    crt, key = generate_client_cert("Rotation-Admin", "admin_valid")
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="/app/certs/ca.crt")
    context.load_cert_chain(certfile=crt, keyfile=key)

    with socket.create_connection(('127.0.0.1', 8443), timeout=2) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            # Valid token: Starts with AA, XOR sum is 0x42
            ssock.sendall(b"ROTATE web AA000000000000E8\n")
            resp = ssock.recv(1024).decode()

            assert resp.startswith("OK "), f"Expected response starting with 'OK ', got: {repr(resp)}"
            parts = resp.strip().split()
            assert len(parts) == 2, "Response should be in format 'OK <password>'"
            password = parts[1]
            assert len(password) == 12, f"Password should be 12 characters, got {len(password)}"
            assert password.isalnum(), "Password should be alphanumeric"

    creds_path = "/home/user/creds.log"
    assert os.path.exists(creds_path), f"Credentials file {creds_path} was not created"

    st = os.stat(creds_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Expected permissions 0600 on {creds_path}, got {oct(perms)}"

    with open(creds_path, "r") as f:
        lines = f.read().splitlines()
        expected_entry = f"web:{password}"
        assert expected_entry in lines, f"Expected entry '{expected_entry}' not found in {creds_path}"