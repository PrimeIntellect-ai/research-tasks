# test_final_state.py

import os
import requests
import socket
import pytest

def test_open_redirect_fixed():
    url = "http://127.0.0.1:8080/login"

    # Test malicious URL
    try:
        res = requests.get(url, params={"redirect_url": "http://malicious.com"}, allow_redirects=False, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert res.status_code == 302, f"Expected HTTP 302, got {res.status_code} for malicious URL"
    assert res.headers.get("Location") == "/home", f"Expected redirect to /home, got {res.headers.get('Location')}"

    # Test valid relative URL
    try:
        res2 = requests.get(url, params={"redirect_url": "/dashboard"}, allow_redirects=False, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert res2.status_code == 302, f"Expected HTTP 302, got {res2.status_code} for valid relative URL"
    assert res2.headers.get("Location") == "/dashboard", f"Expected redirect to /dashboard, got {res2.headers.get('Location')}"

def test_xss_fixed():
    url = "http://127.0.0.1:8080/error"
    payload = "<script>alert(1)</script>"
    try:
        res = requests.get(url, params={"error_msg": payload}, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert res.status_code == 200, f"Expected HTTP 200, got {res.status_code}"
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in res.text, "XSS payload was not properly HTML-entity encoded in the response"
    assert "<script>" not in res.text, "Unescaped '<script>' tag found in the response, XSS vulnerability still present"

def test_csp_header():
    url = "http://127.0.0.1:8080/login"
    try:
        res = requests.get(url, allow_redirects=False, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    expected_csp = "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; frame-ancestors 'none';"
    csp = res.headers.get("Content-Security-Policy")
    assert csp is not None, "Content-Security-Policy header is missing from the response"
    assert csp == expected_csp, f"CSP header mismatch.\nExpected: {expected_csp}\nGot: {csp}"

def test_nginx_block_config():
    block_conf_path = "/home/user/app/nginx/block.conf"
    assert os.path.exists(block_conf_path), f"{block_conf_path} does not exist"

    with open(block_conf_path, "r") as f:
        content = f.read()

    assert "deny 198.51.100.42;" in content, "The malicious IP 198.51.100.42 is not denied in block.conf"

def test_redis_bound_to_localhost():
    redis_conf_path = "/home/user/app/redis/redis.conf"
    assert os.path.exists(redis_conf_path), f"{redis_conf_path} does not exist"

    with open(redis_conf_path, "r") as f:
        content = f.read()

    assert "bind 127.0.0.1" in content, "Redis is not bound to 127.0.0.1 in redis.conf"
    assert "bind 0.0.0.0" not in content, "Redis is still bound to 0.0.0.0 in redis.conf"

    # Verify via socket that Redis is listening on 127.0.0.1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    result = s.connect_ex(('127.0.0.1', 6379))
    s.close()
    assert result == 0, "Redis is not listening on 127.0.0.1:6379"