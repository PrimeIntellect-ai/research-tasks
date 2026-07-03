# test_final_state.py
import os
import re
import urllib.request
import urllib.error
import json

def test_test_results_log():
    log_path = "/home/user/pr_review/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you run pytest and redirect the output?"

    with open(log_path, "r") as f:
        content = f.read()

    # Check for success indicators in pytest output
    assert "failed" not in content.lower() or "0 failed" in content.lower(), "pytest output indicates test failures."
    assert "passed" in content.lower(), "pytest output does not indicate that tests passed."

def test_nginx_conf_updated():
    conf_path = "/home/user/pr_review/nginx.conf"
    assert os.path.isfile(conf_path), f"{conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "underscores_in_headers on;" in content, "nginx.conf does not contain 'underscores_in_headers on;'."

def test_api_via_proxy_limit_10():
    req = urllib.request.Request("http://localhost:8080/resolve")
    req.add_header("Constraint_Limit", "10")

    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode())
            assert "result" in data, "Response JSON missing 'result' key"
    except urllib.error.HTTPError as e:
        assert False, f"HTTP request failed with status {e.code}. Is Nginx stripping the header?"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx proxy: {e.reason}. Are the services running?"

def test_api_via_proxy_limit_0():
    req = urllib.request.Request("http://localhost:8080/resolve")
    req.add_header("Constraint_Limit", "0")

    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode())
            assert "result" in data, "Response JSON missing 'result' key"
            # Depending on the fix, it might return [] or something else, but it shouldn't 500
    except urllib.error.HTTPError as e:
        assert False, f"HTTP request failed with status {e.code}. Did resolver.py fail on limit=0?"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx proxy: {e.reason}. Are the services running?"