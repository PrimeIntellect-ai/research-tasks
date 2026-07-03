# test_final_state.py

import os
import urllib.request
import ssl
import pytest

def test_certificates_exist():
    """Verify that the generated certificate and key exist."""
    assert os.path.isfile("/home/user/cert.pem"), "/home/user/cert.pem does not exist."
    assert os.path.isfile("/home/user/key.pem"), "/home/user/key.pem does not exist."

def test_tls_proxy_functional():
    """Verify that the socat TLS proxy is running on 8443 and forwarding to the legacy service."""
    url = "https://127.0.0.1:8443/"

    # Create an unverified SSL context since it's a self-signed cert
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected status 200 from proxy, got {response.status}"
    except Exception as e:
        pytest.fail(f"Failed to connect to TLS proxy at {url} or it did not return a valid response: {e}")

def test_monitor_c_code():
    """Verify that the monitor.c source code exists and contains required curl elements."""
    c_file = "/home/user/monitor.c"
    assert os.path.isfile(c_file), f"{c_file} does not exist."

    with open(c_file, "r") as f:
        content = f.read()

    assert "<curl/curl.h>" in content, "The C program does not include <curl/curl.h>."
    assert "CURLOPT_SSL_VERIFYPEER" in content, "The C program does not seem to configure CURLOPT_SSL_VERIFYPEER."
    assert "CURLOPT_SSL_VERIFYHOST" in content, "The C program does not seem to configure CURLOPT_SSL_VERIFYHOST."

def test_monitor_binary_exists():
    """Verify that the compiled monitor binary exists."""
    bin_file = "/home/user/monitor"
    assert os.path.isfile(bin_file), f"{bin_file} does not exist."
    assert os.access(bin_file, os.X_OK), f"{bin_file} is not executable."

def test_monitor_log():
    """Verify that the monitor.log exists and contains exactly 3 SUCCESS lines."""
    log_file = "/home/user/monitor.log"
    assert os.path.isfile(log_file), f"{log_file} does not exist. Did you run the monitor?"

    with open(log_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 3, f"Expected exactly 3 lines in {log_file}, but found {len(lines)}."
    for i, line in enumerate(lines):
        assert line == "SUCCESS", f"Line {i+1} in {log_file} is '{line}', expected 'SUCCESS'."