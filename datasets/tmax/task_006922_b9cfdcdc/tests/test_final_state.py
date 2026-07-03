# test_final_state.py
import os
import json
import socket
import pytest

def test_ssh_tunnel_running():
    """Verify that the SSH tunnel is listening on 127.0.0.1:9090."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 9090))
        assert result == 0, "SSH tunnel is not listening on 127.0.0.1:9090."

def test_config_file_exists_and_valid():
    """Verify that the config.json file exists and has the correct content."""
    config_path = "/home/user/proxy/config.json"
    assert os.path.exists(config_path), f"Config file {config_path} does not exist."
    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("config.json is not valid JSON.")

    assert config.get("target_url") == "http://127.0.0.1:9090", "Incorrect target_url in config.json"
    assert config.get("alert_threshold_cpu") == 85, "Incorrect alert_threshold_cpu in config.json"
    assert config.get("smtp_server") == "127.0.0.1:1025", "Incorrect smtp_server in config.json"
    assert config.get("alert_email") == "alerts@dashboard.local", "Incorrect alert_email in config.json"

def test_go_proxy_server_running():
    """Verify that the Go proxy server is listening on 127.0.0.1:7070."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 7070))
        assert result == 0, "Go proxy server is not listening on 127.0.0.1:7070."

def test_alert_log_created_and_valid():
    """Verify that the alert.log file was created and contains the expected log entry."""
    log_path = "/home/user/proxy/alert.log"
    assert os.path.exists(log_path), f"Alert log {log_path} does not exist. Did the proxy trigger the alert?"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "ALERT TRIGGERED: cpu=95" in content, f"Expected alert log entry not found in {log_path}."

def test_email_sent_and_valid():
    """Verify that the email was sent with the correct details."""
    email_log_path = "/home/user/proxy/email_received.log"
    assert os.path.exists(email_log_path), f"Email log {email_log_path} does not exist. Was the email sent?"
    with open(email_log_path, "r") as f:
        email_data = f.read()

    assert "FROM:proxy@dashboard.local" in email_data, "Email FROM address is incorrect or missing."
    assert "TO:alerts@dashboard.local" in email_data, "Email TO address is incorrect or missing."
    assert "High CPU Alert" in email_data, "Email Subject is incorrect or missing."
    assert "CPU usage is at 95%" in email_data, "Email Body is incorrect or missing."