# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_nginx_config_fixed():
    nginx_conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"File {nginx_conf_path} does not exist."
    with open(nginx_conf_path, 'r') as f:
        content = f.read()
    assert "9090" in content, "Nginx config does not seem to be updated to port 9090."
    assert "proxy_pass" in content, "Nginx config is missing proxy_pass directive."

def test_go_app_fixed():
    go_app_path = "/home/user/app/main.go"
    assert os.path.isfile(go_app_path), f"File {go_app_path} does not exist."
    with open(go_app_path, 'r') as f:
        content = f.read()
    assert '9090' in content, "Go app does not seem to be updated to port 9090."

def test_symlink_created():
    symlink_path = "/home/user/public_html/repos"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    resolved_target = os.path.realpath(symlink_path)
    expected_target = "/home/user/repos"
    assert resolved_target == expected_target, f"Symlink points to {resolved_target} instead of {expected_target}"

def test_logrotate_config():
    logrotate_path = "/home/user/logrotate.conf"
    assert os.path.isfile(logrotate_path), f"File {logrotate_path} does not exist."
    with open(logrotate_path, 'r') as f:
        content = f.read()

    assert "/home/user/logs/webhook.log" in content, "logrotate.conf does not target /home/user/logs/webhook.log"

    keywords = ["daily", "rotate 5", "compress", "missingok", "notifempty"]
    for kw in keywords:
        assert kw in content, f"logrotate.conf is missing '{kw}'"

def test_api_reachability_and_logging():
    url = "http://127.0.0.1:8080/api/hook"
    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = response.read().decode('utf-8')
            assert "Success" in body, "Expected 'Success' in response body"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to reach API at {url}: {e}. Ensure Nginx and the Go app are running.")

    log_path = "/home/user/logs/webhook.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Was it created by the webhook?"
    with open(log_path, 'r') as f:
        content = f.read()
    assert "WEBHOOK_RECEIVED" in content, "Log file does not contain 'WEBHOOK_RECEIVED'. The webhook logic might be failing."