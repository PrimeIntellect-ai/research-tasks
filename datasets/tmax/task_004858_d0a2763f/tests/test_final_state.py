# test_final_state.py

import os
import urllib.request
import urllib.error
import base64
import pytest

def test_nginx_conf_fixed_and_secured():
    conf_path = "/home/user/app_stack/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:9091;" in content, "Nginx config proxy_pass port was not fixed to 9091."
    assert 'auth_basic "Restricted Area";' in content, "Nginx config does not contain the required auth_basic directive."
    assert "auth_basic_user_file" in content and ".htpasswd" in content, "Nginx config does not contain the auth_basic_user_file directive pointing to .htpasswd."

def test_htpasswd_file_exists_and_contains_sysadmin():
    htpasswd_path = "/home/user/app_stack/nginx/.htpasswd"
    assert os.path.isfile(htpasswd_path), f"{htpasswd_path} was not created."

    with open(htpasswd_path, 'r') as f:
        content = f.read()

    assert "sysadmin:" in content, "The .htpasswd file does not contain an entry for 'sysadmin'."

def test_manage_auth_script():
    script_path = "/home/user/app_stack/manage_auth.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_test_connection_script_exists():
    script_path = "/home/user/app_stack/test_connection.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

def test_final_result_log():
    log_path = "/home/user/app_stack/final_result.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_log = "HTTP_STATUS: 200, BODY: Backend operational!"
    assert expected_log in content, f"Log file does not contain the expected string. Found: {content}"

def test_live_service_authentication():
    url = "http://127.0.0.1:8080/"

    # First, test without auth to ensure it is protected
    req_unauth = urllib.request.Request(url)
    try:
        urllib.request.urlopen(req_unauth)
        pytest.fail("Service is accessible without authentication, but it should be protected.")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected HTTP 401 Unauthorized without credentials, got {e.code}."
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Nginx on port 8080: {e.reason}")

    # Now test with valid auth
    req_auth = urllib.request.Request(url)
    base64string = base64.b64encode(b'sysadmin:supersecurepass').decode('ascii')
    req_auth.add_header("Authorization", f"Basic {base64string}")

    try:
        response = urllib.request.urlopen(req_auth)
        assert response.getcode() == 200, f"Expected HTTP 200 with valid credentials, got {response.getcode()}."
        body = response.read().decode('utf-8')
        assert "Backend operational!" in body, "Response body did not contain expected backend text."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Authentication failed or backend error. HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Nginx on port 8080: {e.reason}")