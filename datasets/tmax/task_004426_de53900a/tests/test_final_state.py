# test_final_state.py

import os
import time
import socket
import subprocess
import http.client
import pytest

def wait_for_port(port, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return True
        time.sleep(0.1)
    return False

@pytest.fixture(scope="module", autouse=True)
def setup_services():
    procs = []
    # Start auth_service if not running
    if not wait_for_port(8080, timeout=0.5):
        if os.path.exists("/app/auth_service"):
            procs.append(subprocess.Popen(["/app/auth_service"]))
            wait_for_port(8080)

    # Start socat proxy if not running
    if not wait_for_port(9000, timeout=0.5):
        if os.path.exists("/home/user/proxy_worker.sh"):
            procs.append(subprocess.Popen([
                "socat", 
                "TCP-LISTEN:9000,reuseaddr,fork", 
                "EXEC:/home/user/proxy_worker.sh"
            ]))
            wait_for_port(9000)

    yield

    for p in procs:
        p.terminate()

def test_script_exists_and_executable():
    script_path = "/home/user/proxy_worker.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_firewall_rule():
    assert wait_for_port(9000, timeout=2), "Proxy is not listening on port 9000."
    conn = http.client.HTTPConnection("127.0.0.1", 9000, timeout=5)
    conn.request("GET", "/login", headers={"X-Block-Me": "true"})
    res = conn.getresponse()
    assert res.status == 403, f"Firewall rule failed: Expected 403 Forbidden, got {res.status}"
    conn.close()

def test_csp_and_cookies():
    assert wait_for_port(9000, timeout=2), "Proxy is not listening on port 9000."
    conn = http.client.HTTPConnection("127.0.0.1", 9000, timeout=5)
    conn.request("GET", "/login")
    res = conn.getresponse()
    assert res.status == 200, f"Expected 200 OK, got {res.status}"

    csp = res.getheader("Content-Security-Policy", "")
    assert "default-src 'self'" in csp, f"CSP enforcement failed: Header missing or incorrect. Got: {csp}"

    cookie = res.getheader("Set-Cookie", "")
    assert "HttpOnly" in cookie and "Secure" in cookie, f"Cookie inspection failed: Missing HttpOnly or Secure. Got: {cookie}"
    conn.close()

def test_open_redirect_mitigation():
    assert wait_for_port(9000, timeout=2), "Proxy is not listening on port 9000."
    conn = http.client.HTTPConnection("127.0.0.1", 9000, timeout=5)
    conn.request("GET", "/redirect?url=http://evil.com")
    res = conn.getresponse()
    assert res.status == 302, f"Expected 302 Found, got {res.status}"

    loc = res.getheader("Location", "")
    assert loc == "/error", f"Open redirect mitigation failed: Expected Location: /error, got {loc}"
    conn.close()

def test_relative_redirect_allowed():
    assert wait_for_port(9000, timeout=2), "Proxy is not listening on port 9000."
    conn = http.client.HTTPConnection("127.0.0.1", 9000, timeout=5)
    conn.request("GET", "/redirect")
    res = conn.getresponse()
    assert res.status == 302, f"Expected 302 Found, got {res.status}"

    loc = res.getheader("Location", "")
    assert loc == "/dashboard", f"Relative redirect failed: Expected Location: /dashboard, got {loc}"
    conn.close()