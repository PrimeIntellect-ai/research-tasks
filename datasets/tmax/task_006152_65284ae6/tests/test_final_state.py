# test_final_state.py

import os
import ssl
import json
import urllib.request
import urllib.error
import socket
import pytest

def test_ssh_keys_cleaned():
    path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert "legitimate@admin" in content, "Legitimate SSH key was removed."
    assert "hacker@evil" not in content, "Rogue SSH key 'hacker@evil' is still present."

def test_audit_report_created():
    path = "/home/user/audit_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "Vulnerability fixed and mTLS enabled", "Audit report content is incorrect."

def test_certs_generated():
    cert_dir = "/home/user/certs"
    assert os.path.isdir(cert_dir), f"Directory {cert_dir} does not exist"

    expected_files = ["ca.crt", "ca.key", "server.crt", "server.key", "client.crt", "client.key"]
    for f in expected_files:
        file_path = os.path.join(cert_dir, f)
        assert os.path.isfile(file_path), f"Certificate file {file_path} is missing."

def test_server_listening_port_8443():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 8443))
        assert result == 0, "Server is not listening on port 8443."

def test_mtls_and_path_traversal_fix():
    ca_crt = "/home/user/certs/ca.crt"
    client_crt = "/home/user/certs/client.crt"
    client_key = "/home/user/certs/client.key"

    # Ensure certs exist before testing network
    if not (os.path.isfile(ca_crt) and os.path.isfile(client_crt) and os.path.isfile(client_key)):
        pytest.fail("Cannot test mTLS because client/CA certificates are missing.")

    # 1. Test without client cert (should fail)
    context_no_cert = ssl.create_default_context(cafile=ca_crt)
    try:
        urllib.request.urlopen("https://localhost:8443/upload?filename=test.txt", context=context_no_cert, timeout=2)
        pytest.fail("Server accepted connection without a client certificate.")
    except urllib.error.URLError as e:
        # Expected to fail due to SSL handshake error (certificate required)
        pass

    # Setup valid mTLS context
    context_mtls = ssl.create_default_context(cafile=ca_crt)
    context_mtls.load_cert_chain(certfile=client_crt, keyfile=client_key)

    # 2. Test Path Traversal (should return 400)
    req_traversal = urllib.request.Request(
        "https://localhost:8443/upload?filename=../evil.txt",
        data=b"malicious content",
        method="POST"
    )

    try:
        resp = urllib.request.urlopen(req_traversal, context=context_mtls, timeout=2)
        pytest.fail(f"Path traversal attempt succeeded with status {resp.status}, expected 400.")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400 for path traversal, got {e.code}"

    # 3. Test Valid Upload (should succeed)
    req_valid = urllib.request.Request(
        "https://localhost:8443/upload?filename=good.txt",
        data=b"safe content",
        method="POST"
    )

    try:
        resp = urllib.request.urlopen(req_valid, context=context_mtls, timeout=2)
        assert resp.status == 200, f"Expected HTTP 200 for valid upload, got {resp.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Valid upload failed with HTTP {e.code}")

    # Verify file was actually written
    upload_path = "/home/user/app/uploads/good.txt"
    assert os.path.isfile(upload_path), "Valid uploaded file was not saved to the correct directory."
    with open(upload_path, "rb") as f:
        assert f.read() == b"safe content", "Uploaded file content does not match."