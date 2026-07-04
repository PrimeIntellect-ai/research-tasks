# test_final_state.py
import os
import time
import subprocess
import urllib.request
import ssl
import socket

def fetch_https(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
        return response.read().decode('utf-8')

def test_certs_exist():
    """Verify that the certificates exist."""
    assert os.path.isfile("/home/user/certs/cert.pem"), "cert.pem is missing"
    assert os.path.isfile("/home/user/certs/key.pem"), "key.pem is missing"

def test_backends_setup():
    """Verify backend directories and files."""
    for port in [9001, 9002, 9003]:
        health_file = f"/home/user/backend_{port}/health.txt"
        data_file = f"/home/user/backend_{port}/data.txt"

        assert os.path.isfile(health_file), f"Missing {health_file}"
        with open(health_file, "r") as f:
            assert "OK" in f.read(), f"health.txt for {port} does not contain OK"

        assert os.path.isfile(data_file), f"Missing {data_file}"
        with open(data_file, "r") as f:
            assert f"DATA FROM {port}" in f.read(), f"data.txt for {port} does not contain expected string"

def test_proxy_functionality():
    """Verify that the proxy returns data from backends."""
    # Wait a moment to ensure gateway is up
    time.sleep(1)

    responses = set()
    for _ in range(5):
        try:
            res = fetch_https("https://localhost:8443/data.txt")
            if "DATA FROM" in res:
                responses.add(res.strip())
        except Exception as e:
            pass

    assert len(responses) > 0, "Proxy failed to return valid data from backends"

def test_health_check_and_restart():
    """Verify that the gateway detects failures, restarts backends, and logs them."""
    # Kill process on port 9002
    try:
        subprocess.run(["fuser", "-k", "9002/tcp"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    # Wait for health check interval and restart
    time.sleep(5)

    log_file = "/home/user/gateway.log"
    assert os.path.isfile(log_file), "gateway.log is missing"

    with open(log_file, "r") as f:
        log_content = f.read()

    down_msg = "[HEALTH] Backend 9002 is DOWN. Restarting..."
    up_msg = "[HEALTH] Backend 9002 is UP."

    assert down_msg in log_content, f"Did not find restart log for 9002 in gateway.log"
    assert up_msg in log_content, f"Did not find UP log for 9002 in gateway.log"

    # Verify proxy still works
    try:
        res = fetch_https("https://localhost:8443/data.txt")
        assert "DATA FROM" in res, "Proxy failed to return valid data after backend restart"
    except Exception as e:
        assert False, f"Proxy request failed after backend restart: {e}"