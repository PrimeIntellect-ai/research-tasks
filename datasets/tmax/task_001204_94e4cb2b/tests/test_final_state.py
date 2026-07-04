# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_libmathops_so_exists():
    path = "/home/user/project/libmathops.so"
    assert os.path.isfile(path), f"Expected shared library {path} does not exist."

def test_output_log_content():
    path = "/home/user/project/output.log"
    assert os.path.isfile(path), f"Expected output log {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "95682642", f"Output log content is incorrect. Expected '95682642', got '{content}'."

def test_nginx_proxy_and_python_server():
    # Test the proxy and the python server using the original hex string
    url = "http://127.0.0.1:9090/api/hash?data=776f726c64"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            body = response.read().decode('utf-8').strip()
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy at {url}: {e}")

    assert status == 200, f"Expected HTTP status 200, got {status}."
    assert body == "95682642", f"Expected response body '95682642', got '{body}'."

def test_nginx_proxy_and_python_server_dynamic():
    # Test with another hex string '48656c6c6f' ("Hello")
    # H=72, e=101, l=108, l=108, o=111
    # Hash: 72*1 + 101*31 + 108*961 + 108*29791 + 111*923521 = 105835250
    url = "http://127.0.0.1:9090/api/hash?data=48656c6c6f"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            body = response.read().decode('utf-8').strip()
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy at {url}: {e}")

    assert status == 200, f"Expected HTTP status 200, got {status}."
    assert body == "105835250", f"Expected response body '105835250', got '{body}'."