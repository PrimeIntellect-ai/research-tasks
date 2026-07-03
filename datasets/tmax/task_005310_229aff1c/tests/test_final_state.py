# test_final_state.py
import os
import requests
import pytest

def test_compromised_ips_file():
    path = "/home/user/compromised_ips.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The intrusion detection script may not have run or failed to output to the correct location."

    with open(path, "r") as f:
        content = [line.strip() for line in f.read().splitlines() if line.strip()]

    expected_ips = ["10.0.0.42", "172.16.0.100", "192.168.1.55"]
    assert content == expected_ips, f"Expected IPs {expected_ips}, but got {content} in {path}. Ensure IPs are sorted and deduplicated."

def test_security_headers():
    url = "http://127.0.0.1:8080/"
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {url}. Are the services running? Error: {e}")

    headers = response.headers

    # Strict-Transport-Security
    sts = headers.get("Strict-Transport-Security", "")
    assert "max-age=31536000" in sts, f"Strict-Transport-Security header missing or incorrect max-age. Got: '{sts}'"
    assert "includeSubDomains" in sts.replace(" ", ""), f"Strict-Transport-Security header missing includeSubDomains. Got: '{sts}'"

    # X-Content-Type-Options
    xcto = headers.get("X-Content-Type-Options", "")
    assert xcto.lower() == "nosniff", f"X-Content-Type-Options header missing or incorrect. Got: '{xcto}'"

def test_cookie_security():
    url = "http://127.0.0.1:8080/login"
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    set_cookie = response.headers.get("Set-Cookie", "")
    if not set_cookie:
        # Fallback to checking the root if /login doesn't set a cookie
        response = requests.get("http://127.0.0.1:8080/", timeout=5, allow_redirects=False)
        set_cookie = response.headers.get("Set-Cookie", "")

    if set_cookie:
        assert "Secure" in set_cookie or "secure" in set_cookie, f"Set-Cookie header missing Secure flag. Got: '{set_cookie}'"
        assert "HttpOnly" in set_cookie or "httponly" in set_cookie.lower(), f"Set-Cookie header missing HttpOnly flag. Got: '{set_cookie}'"
    else:
        # If no cookie is returned by the backend, we check the Nginx config as a fallback
        nginx_conf_path = "/app/proxy/nginx.conf"
        assert os.path.exists(nginx_conf_path), "Nginx config missing."
        with open(nginx_conf_path, "r") as f:
            conf = f.read()
        assert "proxy_cookie_path" in conf or "proxy_cookie_flags" in conf, "Nginx config does not contain proxy_cookie_path or proxy_cookie_flags to secure cookies."

def test_path_traversal_mitigation():
    url = "http://127.0.0.1:8080/upload"
    files = {'file': ('../../../tmp/evil.txt', b'malicious content')}

    evil_file_path = "/tmp/evil.txt"
    if os.path.exists(evil_file_path):
        os.remove(evil_file_path)

    try:
        response = requests.post(url, files=files, timeout=5, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert not os.path.exists(evil_file_path), f"Path traversal successful: file was written outside the uploads directory to {evil_file_path}"

    # The application should either reject the request or safely save the file in /app/uploads
    # We just ensure it didn't write to /tmp/evil.txt.
    if os.path.exists(evil_file_path):
        os.remove(evil_file_path)