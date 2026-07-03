# test_final_state.py

import os
import base64
import urllib.request
import urllib.error
import time
import pytest

def get_expected_plaintext():
    v1_path = "/home/user/v1.txt"
    v2_path = "/home/user/v2.txt"

    with open(v1_path, "r") as f:
        v1_lines = set(line.strip() for line in f if line.strip())

    with open(v2_path, "r") as f:
        v2_lines = [line.strip() for line in f if line.strip()]

    new_lines = [line for line in v2_lines if line not in v1_lines]
    new_lines.sort()

    return "\n".join(new_lines)

def test_release_diff_b64_content():
    path = "/home/user/release_diff.b64"
    assert os.path.exists(path), f"File {path} does not exist."

    expected_plaintext = get_expected_plaintext()
    expected_b64 = base64.b64encode(expected_plaintext.encode('utf-8')).decode('utf-8')

    with open(path, "r") as f:
        actual_b64 = f.read().strip()

    assert actual_b64 == expected_b64, "The base64 content in release_diff.b64 does not match the expected output."

def test_nginx_proxy_forbidden_without_auth():
    req = urllib.request.Request("http://127.0.0.1:8080/")
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected HTTP Error 403, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected HTTP 403 Forbidden, got {e.code}"

def test_nginx_proxy_success_with_auth():
    req = urllib.request.Request("http://127.0.0.1:8080/")
    req.add_header("X-Release-Auth", "YXBwcm92ZWQ=")

    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200 OK, got {response.status}"
            content = response.read().decode('utf-8').strip()
            expected_plaintext = get_expected_plaintext()
            assert content == expected_plaintext, "The decoded plaintext from the server does not match the expected output."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected HTTP 200 OK, but got HTTPError {e.code}")

def test_nginx_rate_limiting():
    # Rate limit is 30 req/min, burst 5. Sending ~10 rapid requests should trigger a 503.
    req = urllib.request.Request("http://127.0.0.1:8080/")
    req.add_header("X-Release-Auth", "YXBwcm92ZWQ=")

    status_codes = []
    for _ in range(15):
        try:
            with urllib.request.urlopen(req) as response:
                status_codes.append(response.status)
        except urllib.error.HTTPError as e:
            status_codes.append(e.code)

    assert 503 in status_codes, "Expected HTTP 503 Service Unavailable due to rate limiting, but it was not triggered."