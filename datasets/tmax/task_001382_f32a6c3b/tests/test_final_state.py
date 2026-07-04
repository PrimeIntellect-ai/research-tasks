# test_final_state.py

import os
import urllib.request
import urllib.error

def test_files_exist():
    assert os.path.exists("/home/user/mock_api"), "Rust project directory /home/user/mock_api does not exist."
    assert os.path.exists("/home/user/nginx.conf"), "Nginx config /home/user/nginx.conf does not exist."

def test_nginx_and_rust_server_integration():
    url = "http://127.0.0.1:8080/legacy"

    # Test case 1: Basic functionality
    payload1 = b"+A+A+B-A?A?B+C-C?C"
    req1 = urllib.request.Request(url, data=payload1, method='POST')
    try:
        with urllib.request.urlopen(req1, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            headers = dict(response.getheaders())
            assert "X-Mock-Proxy" in headers, "Missing X-Mock-Proxy header in response."
            assert headers["X-Mock-Proxy"] == "Active", f"Expected X-Mock-Proxy: Active, got {headers['X-Mock-Proxy']}"

            body = response.read().decode('utf-8').strip()
            assert body == "1,1,0", f"Expected body '1,1,0', got '{body}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx at {url}: {e}"

    # Test case 2: Whitespace ignoring and negative tallies
    payload2 = b" + A \n+ B - A ?A \t ?B -C -C ?C"
    req2 = urllib.request.Request(url, data=payload2, method='POST')
    try:
        with urllib.request.urlopen(req2, timeout=5) as response:
            body = response.read().decode('utf-8').strip()
            assert body == "0,1,-2", f"Expected body '0,1,-2' (ignoring whitespace), got '{body}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx at {url}: {e}"

    # Test case 3: Abort on invalid character
    payload3 = b"+A+B?A?B ! +A?A"
    req3 = urllib.request.Request(url, data=payload3, method='POST')
    try:
        with urllib.request.urlopen(req3, timeout=5) as response:
            body = response.read().decode('utf-8').strip()
            assert body == "1,1", f"Expected body '1,1' (aborted before second ?A), got '{body}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx at {url}: {e}"