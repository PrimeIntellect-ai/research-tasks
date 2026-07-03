# test_final_state.py
import os
import urllib.request
import urllib.error
import socket

def test_files_exist():
    """Test that all required files have been created."""
    required_files = [
        "/home/user/waf/waf.h",
        "/home/user/waf/waf.c",
        "/home/user/waf/proxy.go",
        "/home/user/test_waf.sh",
        "/home/user/waf_test.log"
    ]
    for file_path in required_files:
        assert os.path.exists(file_path), f"Required file {file_path} is missing."
        assert os.path.isfile(file_path), f"Path {file_path} exists but is not a regular file."

def test_ports_listening():
    """Test that the proxy is listening on port 8080 and backend on 9090."""
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    assert is_port_open(8080), "Proxy is not listening on port 8080."
    assert is_port_open(9090), "Backend server is not listening on port 9090."

def get_http_response(url):
    """Helper to get HTTP response status and body."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return response.getcode(), response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except urllib.error.URLError as e:
        return None, str(e)

def test_proxy_behavior_safe_requests():
    """Test that safe requests are forwarded and not blocked."""
    safe_urls = [
        "http://127.0.0.1:8080/",
        "http://127.0.0.1:8080/union_select",
        "http://127.0.0.1:8080/products?search=apple",
        "http://127.0.0.1:8080/union_and_select"
    ]
    for url in safe_urls:
        status, _ = get_http_response(url)
        assert status is not None, f"Failed to connect to proxy for URL: {url}"
        assert status != 403, f"Safe URL {url} was incorrectly blocked with status 403."

def test_proxy_behavior_malicious_requests():
    """Test that malicious requests are blocked with 403 and correct body."""
    malicious_urls = [
        "http://127.0.0.1:8080/?q=union%20select",
        "http://127.0.0.1:8080/?q=UnIoN%20%20%20sElEcT",
        "http://127.0.0.1:8080/items?q=UnIoN%20%20%20sElEcT%20*",
        "http://127.0.0.1:8080/?test=union%20select"
    ]
    for url in malicious_urls:
        status, body = get_http_response(url)
        assert status is not None, f"Failed to connect to proxy for URL: {url}"
        assert status == 403, f"Malicious URL {url} was not blocked. Expected 403, got {status}."
        assert body.strip() == "Blocked by WAF", f"Incorrect block body for URL {url}. Expected 'Blocked by WAF', got '{body.strip()}'."

def test_waf_test_log_contents():
    """Test that the waf_test.log contains the correct sequence of HTTP status codes."""
    log_file = "/home/user/waf_test.log"
    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in {log_file}, found {len(lines)}."

    # Line 1: Safe
    assert lines[0] != "403", f"Line 1 in {log_file} should not be 403, got {lines[0]}."
    # Line 2: Blocked
    assert lines[1] == "403", f"Line 2 in {log_file} should be 403, got {lines[1]}."
    # Line 3: Safe
    assert lines[2] != "403", f"Line 3 in {log_file} should not be 403, got {lines[2]}."
    # Line 4: Blocked
    assert lines[3] == "403", f"Line 4 in {log_file} should be 403, got {lines[3]}."