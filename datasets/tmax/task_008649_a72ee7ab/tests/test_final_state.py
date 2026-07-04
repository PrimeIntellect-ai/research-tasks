# test_final_state.py

import os
import pytest

def test_nginx_config_backup():
    bak_path = "/home/user/nginx/nginx.conf.bak"
    assert os.path.isfile(bak_path), f"Backup file missing: {bak_path}"
    with open(bak_path, 'r') as f:
        content = f.read()
    assert "8081" in content, "Backup file does not contain the original port 8081"

def test_nginx_config_updated():
    conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config missing: {conf_path}"
    with open(conf_path, 'r') as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:8080;" in content, "Nginx config does not contain the updated port 8080"

def test_storage_quota_backup():
    bak_path = "/home/user/backend/data.db.bak"
    assert os.path.isfile(bak_path), f"Database backup missing: {bak_path}"
    size = os.path.getsize(bak_path)
    expected_size = 2 * 1024 * 1024
    assert size == expected_size, f"Database backup size is {size}, expected {expected_size} bytes"

def test_storage_quota_original():
    db_path = "/home/user/backend/data.db"
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        assert size <= 1024 * 1024, f"Database file is too large: {size} bytes (must be <= 1MB)"

def test_timezone_profile():
    env_path = "/home/user/.backend_env"
    assert os.path.isfile(env_path), f"Environment profile missing: {env_path}"
    with open(env_path, 'r') as f:
        content = f.read().strip()
    assert 'export TZ="Europe/London"' in content, "Environment profile does not contain the correct TZ export"

def test_run_script_exists():
    script_path = "/home/user/run.py"
    assert os.path.isfile(script_path), f"Run script missing: {script_path}"

def test_resolution_log():
    log_path = "/home/user/resolution.log"
    assert os.path.isfile(log_path), f"Resolution log missing: {log_path}"
    with open(log_path, 'r') as f:
        content = f.read().strip()
    expected = "Backend successfully started on port 8080"
    assert expected in content, f"Resolution log does not contain the expected success message. Found: {content}"