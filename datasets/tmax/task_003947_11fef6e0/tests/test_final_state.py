# test_final_state.py

import os
import requests
import pytest

def test_makefile_fixed():
    path = "/app/vendor/simple-c-server-1.0/Makefile"
    assert os.path.isfile(path), f"Makefile missing at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "-lthred" not in content, "Makefile still contains typo '-lthred'."
    assert "-lpthread" in content, "Makefile does not contain the correct '-lpthread' flag."

def test_nginx_config_fixed():
    path = "/app/nginx/nginx.conf"
    assert os.path.isfile(path), f"Nginx config missing at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:9000;" in content, "Nginx config does not have the correct proxy_pass to port 9000."
    assert "proxy_pass http://127.0.0.1:9999;" not in content, "Nginx config still has the incorrect proxy_pass to port 9999."

def test_ci_runner_fixed():
    path = "/app/ci_runner.sh"
    assert os.path.isfile(path), f"CI runner script missing at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "TZ=Etc/UTC" in content, "CI runner script does not set TZ=Etc/UTC."

def test_service_is_running_and_proxying():
    url = "http://127.0.0.1:8080/status"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    assert "Status: OK" in response.text, f"Expected body to contain 'Status: OK', got {response.text!r}"