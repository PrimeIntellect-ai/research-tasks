# test_final_state.py
import os
import subprocess
import re
import pytest

def test_bashrc_env_vars():
    """Check that the required environment variables are defined in .bashrc."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"{bashrc_path} does not exist"

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert re.search(r'BACKEND_1\s*=\s*["\']?127\.0\.0\.1:9001["\']?', content), "BACKEND_1 not correctly set in .bashrc"
    assert re.search(r'BACKEND_2\s*=\s*["\']?127\.0\.0\.1:9002["\']?', content), "BACKEND_2 not correctly set in .bashrc"
    assert re.search(r'FRONTEND_PORT\s*=\s*["\']?8443["\']?', content), "FRONTEND_PORT not correctly set in .bashrc"

def test_tls_certificates():
    """Verify the self-signed certificate and key."""
    cert_path = "/home/user/certs/proxy.crt"
    key_path = "/home/user/certs/proxy.key"

    assert os.path.exists(cert_path), f"Certificate {cert_path} not found"
    assert os.path.exists(key_path), f"Private key {key_path} not found"

    # Check Common Name
    subject_cmd = ["openssl", "x509", "-in", cert_path, "-noout", "-subject"]
    subject_result = subprocess.run(subject_cmd, capture_output=True, text=True)
    assert subject_result.returncode == 0, "Failed to read certificate subject"
    assert "CN = localhost" in subject_result.stdout or "CN=localhost" in subject_result.stdout, "Certificate Common Name (CN) is not localhost"

    # Check Modulus match
    cert_mod_cmd = ["openssl", "x509", "-noout", "-modulus", "-in", cert_path]
    key_mod_cmd = ["openssl", "rsa", "-noout", "-modulus", "-in", key_path]

    cert_mod = subprocess.run(cert_mod_cmd, capture_output=True, text=True).stdout.strip()
    key_mod = subprocess.run(key_mod_cmd, capture_output=True, text=True).stdout.strip()

    assert cert_mod != "", "Failed to get certificate modulus"
    assert cert_mod == key_mod, "Certificate and private key do not match"

def test_nginx_config_syntax():
    """Verify the NGINX configuration syntax."""
    conf_path = "/home/user/nginx-dev.conf"
    assert os.path.exists(conf_path), f"NGINX config {conf_path} not found"

    cmd = ["nginx", "-t", "-c", conf_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"NGINX configuration syntax is invalid:\n{result.stderr}"

def test_nginx_config_contents():
    """Check that the NGINX configuration contains the required directives."""
    conf_path = "/home/user/nginx-dev.conf"
    assert os.path.exists(conf_path), f"NGINX config {conf_path} not found"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "daemon off;" in content, "Directive 'daemon off;' is missing"
    assert "/home/user/nginx.pid" in content, "PID file path '/home/user/nginx.pid' is missing"
    assert "/home/user/error.log" in content, "Error log path '/home/user/error.log' is missing"
    assert "/home/user/access.log" in content, "Access log path '/home/user/access.log' is missing"
    assert "127.0.0.1:9001" in content, "Backend 1 (127.0.0.1:9001) is missing from config"
    assert "127.0.0.1:9002" in content, "Backend 2 (127.0.0.1:9002) is missing from config"
    assert re.search(r'listen\s+8443\s+ssl', content), "Server is not listening on 8443 with ssl"
    assert "proxy.crt" in content, "Certificate 'proxy.crt' is not referenced"
    assert "proxy.key" in content, "Private key 'proxy.key' is not referenced"
    assert "proxy_pass" in content and "http://microservices" in content, "proxy_pass to http://microservices is missing"