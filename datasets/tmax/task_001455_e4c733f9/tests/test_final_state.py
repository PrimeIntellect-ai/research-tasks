# test_final_state.py
import os
import json
import re
import urllib.request
import ssl
import pytest

def test_directories_and_config():
    directories = [
        "/home/user/app",
        "/home/user/certs",
        "/home/user/config",
        "/home/user/mailbox"
    ]
    for directory in directories:
        assert os.path.isdir(directory), f"Directory {directory} does not exist"

    config_path = "/home/user/config/settings.json"
    assert os.path.isfile(config_path), f"Configuration file {config_path} does not exist"

    with open(config_path, "r") as f:
        try:
            config_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {config_path} does not contain valid JSON")

    assert config_data.get("admin_email") == "sysadmin@local.domain", "admin_email in settings.json is incorrect"

def test_deploy_sh_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_tls_certs_exist():
    assert os.path.isfile("/home/user/certs/cert.pem"), "cert.pem does not exist"
    assert os.path.isfile("/home/user/certs/key.pem"), "key.pem does not exist"

def test_startup_log():
    log_path = "/home/user/app/startup.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist"

    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) >= 1, f"Log file {log_path} is empty"
    last_line = lines[-1].strip()

    # Simple RFC3339 regex matching timezone offset +01:00 or +02:00
    # e.g., 2023-10-25T14:30:00+02:00
    pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?\+(01:00|02:00)$"
    assert re.match(pattern, last_line), f"Timestamp '{last_line}' is not a valid RFC3339 string with Europe/Copenhagen offset (+01:00 or +02:00)"

def test_server_running():
    url = "https://127.0.0.1:9443/health"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.getcode() == 200, f"Expected HTTP 200, got {response.getcode()}"
            body = response.read().decode("utf-8")
            try:
                data = json.loads(body)
                assert data.get("status") == "ok", "Expected JSON {'status': 'ok'}"
            except json.JSONDecodeError:
                pytest.fail("Response body is not valid JSON")
    except Exception as e:
        pytest.fail(f"Failed to connect to the Go web server at {url}: {e}")

def test_alert_eml():
    eml_path = "/home/user/mailbox/alert.eml"
    assert os.path.isfile(eml_path), f"Email file {eml_path} does not exist"

    with open(eml_path, "r") as f:
        content = f.read()

    expected_content = "To: sysadmin@local.domain\nSubject: Alert\n\nService notification triggered.\n"
    assert content.strip() == expected_content.strip(), "Contents of alert.eml do not match the expected output"