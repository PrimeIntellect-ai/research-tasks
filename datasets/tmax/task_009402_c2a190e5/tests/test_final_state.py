# test_final_state.py
import os
import subprocess
import time
import ssl
import http.client
import pytest

def test_task_complete_marker():
    assert os.path.isfile("/home/user/task_complete"), "Task complete marker not found at /home/user/task_complete."

def test_tls_certificates():
    key_path = "/home/user/certs/server.key"
    crt_path = "/home/user/certs/server.crt"
    assert os.path.isfile(key_path), f"TLS private key not found at {key_path}."
    assert os.path.isfile(crt_path), f"TLS certificate not found at {crt_path}."

    # Check CN
    out = subprocess.check_output(["openssl", "x509", "-in", crt_path, "-noout", "-subject"], text=True)
    assert "CN = localhost" in out or "CN=localhost" in out, "Certificate Common Name (CN) is not localhost."

def test_rust_server_behavior():
    # Build the server
    build_proc = subprocess.run(
        ["cargo", "build", "--release"], 
        cwd="/home/user/auth-server", 
        capture_output=True, 
        text=True
    )
    assert build_proc.returncode == 0, f"Cargo build failed:\n{build_proc.stderr}"

    # Run the server
    server_proc = subprocess.Popen(
        ["./target/release/auth-server"], 
        cwd="/home/user/auth-server",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for server to start
    time.sleep(3)

    try:
        # Create unverified context for self-signed cert
        ctx = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection("127.0.0.1", 8443, context=ctx, timeout=5)

        # Test Open Redirect Fix
        conn.request("GET", "/login?next=http://evil.com")
        res_evil = conn.getresponse()
        loc_evil = res_evil.getheader("Location")
        res_evil.read()  # Consume response

        assert loc_evil != "http://evil.com", "Open redirect vulnerability is still present."
        assert loc_evil == "/dashboard", f"Expected fallback redirect to /dashboard for malicious URL, got {loc_evil}"

        # Test valid relative redirect
        conn.request("GET", "/login?next=/profile")
        res_valid = conn.getresponse()
        loc_valid = res_valid.getheader("Location")
        csp_header = res_valid.getheader("Content-Security-Policy")
        res_valid.read()  # Consume response

        assert loc_valid == "/profile", f"Valid relative redirect broken. Expected /profile, got {loc_valid}"

        # Test CSP Header
        assert csp_header is not None, "Content-Security-Policy header is missing from the response."
        assert "default-src 'self'" in csp_header, f"Content-Security-Policy header is incorrect. Got: {csp_header}"

        conn.close()
    finally:
        server_proc.terminate()
        server_proc.wait()