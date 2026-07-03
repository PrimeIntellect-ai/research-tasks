# test_final_state.py

import os
import json
import urllib.request
import urllib.parse
import urllib.error
import socket
import pytest

def test_audit_trail_exists_and_valid():
    audit_file = "/home/user/audit_trail.json"
    assert os.path.isfile(audit_file), f"Audit trail file not found at {audit_file}"

    with open(audit_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Audit trail is not valid JSON")

    expected_vulns = ["SQL_Injection", "Reflected_XSS", "Insecure_Cookie", "Weak_Password_Hashing"]
    assert "vulnerabilities_fixed" in data, "Missing 'vulnerabilities_fixed' in audit trail"
    assert sorted(data["vulnerabilities_fixed"]) == sorted(expected_vulns), "Incorrect vulnerabilities_fixed list"

    assert data.get("hashing_algorithm_implemented") == "SHA-256", "Incorrect hashing algorithm in audit trail"

    assert "cookie_flags_added" in data, "Missing 'cookie_flags_added' in audit trail"
    assert sorted(data["cookie_flags_added"]) == sorted(["HttpOnly", "Secure"]), "Incorrect cookie flags in audit trail"

def test_server_running_on_8080():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "Server is not listening on port 8080. Ensure it was started in the background."

def test_sql_injection_fixed():
    url = "http://127.0.0.1:8080/login"
    data = urllib.parse.urlencode({'username': "admin' OR '1'='1", 'password': 'wrong'}).encode('utf-8')
    req = urllib.request.Request(url, data=data)

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
    except urllib.error.HTTPError as e:
        status = e.code
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to server at /login: {e}")

    assert status == 401, f"Expected 401 Unauthorized for SQL injection attempt, got {status}. SQLi is likely not fixed."

def test_crypto_and_cookie_fixed():
    url = "http://127.0.0.1:8080/login"
    data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin'}).encode('utf-8')
    req = urllib.request.Request(url, data=data)

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            headers = response.info()
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected 200 OK for valid credentials, got {e.code}. Password hashing might be incorrect.")
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to server at /login: {e}")

    assert status == 200, f"Expected 200 OK for valid credentials, got {status}"

    set_cookie = headers.get('Set-Cookie', '')
    assert 'HttpOnly' in set_cookie, "Set-Cookie header is missing the HttpOnly flag"
    assert 'Secure' in set_cookie, "Set-Cookie header is missing the Secure flag"

def test_xss_fixed():
    url = "http://127.0.0.1:8080/greet?name=%3Cscript%3Ealert(1)%3C/script%3E"
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            body = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to server at /greet: {e}")

    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in body, "XSS payload was not correctly HTML entity encoded"
    assert "<script>" not in body, "Unencoded <script> tag found in response, XSS vulnerability is still present"