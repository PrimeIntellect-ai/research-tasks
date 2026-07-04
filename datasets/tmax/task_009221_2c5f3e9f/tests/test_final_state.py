# test_final_state.py

import os
import subprocess
import sqlite3
import re
import pytest

def test_cargo_compiles_successfully():
    """Test that the Rust project compiles successfully without errors."""
    app_dir = "/home/user/app"
    assert os.path.isdir(app_dir), f"Directory {app_dir} does not exist."

    result = subprocess.run(
        ["cargo", "check"],
        cwd=app_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Cargo check failed:\n{result.stderr}"

def test_password_validation_logic():
    """Test that the password length validation is updated to 12."""
    api_rs_path = "/home/user/app/src/api.rs"
    assert os.path.isfile(api_rs_path), f"File {api_rs_path} does not exist."

    with open(api_rs_path, "r") as f:
        content = f.read()

    # Check for < 12 or <= 11 logic
    assert re.search(r'<\s*12', content) or re.search(r'<=\s*11', content), \
        "Password length validation constraint was not updated to 12 characters."

def test_database_schema_migrated():
    """Test that the schema was applied to data.db and the users table exists."""
    db_path = "/home/user/app/data.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table = cursor.fetchone()
    conn.close()

    assert table is not None, "The 'users' table does not exist in data.db."

def test_nginx_configuration_valid():
    """Test that the Nginx configuration is valid."""
    nginx_conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"File {nginx_conf_path} does not exist."

    result = subprocess.run(
        ["nginx", "-t", "-c", nginx_conf_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Nginx configuration test failed:\n{result.stderr}"

def test_nginx_rate_limiting_configured():
    """Test that the Nginx configuration contains the correct rate limiting directives."""
    nginx_conf_path = "/home/user/nginx.conf"
    with open(nginx_conf_path, "r") as f:
        content = f.read()

    # Check for limit_req_zone
    assert re.search(r'limit_req_zone\s+\$binary_remote_addr\s+zone=api_limit:10m\s+rate=5r/s\s*;', content), \
        "Nginx config is missing the correct limit_req_zone directive."

    # Check for limit_req
    assert re.search(r'limit_req\s+zone=api_limit\s+burst=10\s+nodelay\s*;', content), \
        "Nginx config is missing the correct limit_req directive in the location block."

def test_status_log_success():
    """Test that the status.log file contains SUCCESS."""
    status_log_path = "/home/user/status.log"
    assert os.path.isfile(status_log_path), f"File {status_log_path} does not exist."

    with open(status_log_path, "r") as f:
        content = f.read().strip()

    assert content == "SUCCESS", f"Expected 'SUCCESS' in status.log, but found '{content}'."