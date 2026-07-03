# test_final_state.py

import os
import sqlite3
import subprocess
import json

def test_directories_exist():
    for d in ["/home/user/data", "/home/user/tls", "/home/user/web"]:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_sqlite_database():
    db_path = "/home/user/data/users.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    assert cursor.fetchone() is not None, "Table 'users' does not exist in the database."

    # Check records
    cursor.execute("SELECT username, group_name FROM users ORDER BY username")
    rows = cursor.fetchall()

    expected_rows = [("mailer", "mail"), ("webadmin", "wheel")]
    assert rows == expected_rows, f"Expected users {expected_rows}, but got {rows}."

    conn.close()

def test_tls_certificates():
    cert_path = "/home/user/tls/cert.pem"
    key_path = "/home/user/tls/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Key file {key_path} does not exist."

    # Check Common Name (CN)
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout", "-subject"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to read certificate with openssl."
    assert "CN = localhost" in result.stdout or "CN=localhost" in result.stdout, "Certificate Common Name (CN) is not 'localhost'."

def test_app_py_ssl_logic():
    app_path = "/home/user/web/app.py"
    assert os.path.isfile(app_path), f"Web server script {app_path} does not exist."

    with open(app_path, "r") as f:
        content = f.read()

    assert "ssl.SSLContext" in content or "ssl.wrap_socket" in content, "Web server script does not appear to use the ssl module for HTTPS."

def test_dockerfile():
    dockerfile_path = "/home/user/web/Dockerfile"
    assert os.path.isfile(dockerfile_path), f"Dockerfile {dockerfile_path} does not exist."

    with open(dockerfile_path, "r") as f:
        content = f.read()

    assert "FROM python:3.10-slim" in content, "Dockerfile does not use python:3.10-slim as the base image."
    assert "USER appuser" in content, "Dockerfile does not switch to USER appuser."
    assert "EXPOSE 9443" in content, "Dockerfile does not EXPOSE port 9443."

def test_verification_log():
    log_path = "/home/user/verification.log"
    assert os.path.isfile(log_path), f"Verification log {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert '{"status": "ok"}' in content, "Verification log does not contain the exact expected JSON payload."