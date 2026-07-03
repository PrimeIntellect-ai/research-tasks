# test_final_state.py

import os
import re
import socket
import subprocess
import pytest

def test_tls_certificates_exist():
    cert_path = "/home/user/microservices/certs/cert.pem"
    key_path = "/home/user/microservices/certs/key.pem"
    assert os.path.isfile(cert_path), f"Certificate file missing: {cert_path}"
    assert os.path.isfile(key_path), f"Key file missing: {key_path}"

def test_nginx_config_content():
    conf_path = "/home/user/microservices/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config missing: {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert re.search(r"listen\s+8443\s+ssl", content) or re.search(r"listen\s+.*8443.*ssl", content), "Nginx config missing 'listen 8443 ssl'"
    assert "cert.pem" in content, "Nginx config missing cert.pem reference"
    assert "key.pem" in content, "Nginx config missing key.pem reference"
    assert "root /home/user/microservices/www" in content or "root\s+/home/user/microservices/www" in content, "Nginx config missing correct root directive"
    assert "nginx.pid" in content, "Nginx config missing pid directive"
    assert "nginx_access.log" in content, "Nginx config missing access_log directive"
    assert "nginx_error.log" in content, "Nginx config missing error_log directive"

def test_supervisord_config_content():
    conf_path = "/home/user/microservices/supervisord.conf"
    assert os.path.isfile(conf_path), f"Supervisord config missing: {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "[program:webapp]" in content, "Supervisord config missing [program:webapp]"
    assert "[program:mailer]" in content, "Supervisord config missing [program:mailer]"
    assert "autorestart" in content.lower(), "Supervisord config missing autorestart directives"
    assert "supervisord.log" in content, "Supervisord config missing log directive"
    assert "supervisord.pid" in content, "Supervisord config missing pid directive"

def test_processes_running():
    try:
        ps_output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute 'ps aux'")

    assert "supervisord" in ps_output, "supervisord is not running"
    assert "nginx" in ps_output, "nginx is not running"
    assert "mailer.sh" in ps_output or "nc -l -p 8025" in ps_output, "mailer script is not running"

def test_ports_listening():
    # Check port 8443
    s8443 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result8443 = s8443.connect_ex(('127.0.0.1', 8443))
    s8443.close()
    assert result8443 == 0, "Port 8443 (nginx) is not listening"

    # Check port 8025
    s8025 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result8025 = s8025.connect_ex(('127.0.0.1', 8025))
    s8025.close()
    assert result8025 == 0, "Port 8025 (mailer) is not listening"

def test_status_log_content():
    log_path = "/home/user/status.log"
    assert os.path.isfile(log_path), f"Status log missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert re.search(r"webapp\s+RUNNING", content), "Status log does not show webapp as RUNNING"
    assert re.search(r"mailer\s+RUNNING", content), "Status log does not show mailer as RUNNING"