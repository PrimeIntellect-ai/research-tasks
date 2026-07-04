# test_final_state.py

import os
import urllib.request
import ssl
import subprocess
import time

def test_go_app_fixed_and_compiled():
    main_go = "/home/user/app/main.go"
    main_bin = "/home/user/app/main"

    assert os.path.isfile(main_go), f"{main_go} is missing."
    with open(main_go, "r") as f:
        content = f.read()
    assert '127.0.0.1:9090' in content, f"{main_go} does not seem to listen on 127.0.0.1:9090."
    assert '127.0.0.1:80' not in content, f"{main_go} is still trying to bind to port 80."

    assert os.path.isfile(main_bin), f"Compiled Go binary {main_bin} is missing."
    assert os.access(main_bin, os.X_OK), f"{main_bin} is not executable."

def test_tls_certs_exist():
    crt_file = "/home/user/certs/server.crt"
    key_file = "/home/user/certs/server.key"

    assert os.path.isfile(crt_file), f"TLS certificate {crt_file} is missing."
    assert os.path.isfile(key_file), f"TLS private key {key_file} is missing."

def test_nginx_config_updated():
    nginx_conf = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf), f"{nginx_conf} is missing."

    with open(nginx_conf, "r") as f:
        content = f.read()

    assert "8080" not in content, "Nginx is still configured to listen on port 8080."
    assert "8443" in content, "Nginx is not configured to listen on port 8443."
    assert "ssl_certificate " in content or "ssl_certificate\t" in content or "ssl_certificate\n" in content or "listen 8443 ssl" in content or "ssl " in content, "Nginx is not configured for SSL/TLS."

def test_monitor_script_exists_and_executable():
    script = "/home/user/monitor.sh"
    assert os.path.isfile(script), f"{script} is missing."
    assert os.access(script, os.X_OK), f"{script} is not executable."

def test_success_txt():
    success_file = "/home/user/success.txt"
    assert os.path.isfile(success_file), f"{success_file} is missing."

    with open(success_file, "r") as f:
        content = f.read().strip()

    assert "Go Backend Online" in content, f"{success_file} does not contain the expected output."

def test_services_running_and_responding():
    # Test if we can actually reach the API through Nginx
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:8443/api"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            body = response.read().decode('utf-8')
            assert "Go Backend Online" in body, f"Expected 'Go Backend Online' from {url}, got '{body}'"
    except Exception as e:
        assert False, f"Failed to connect to Nginx at {url} or received an error: {e}"

def test_go_backend_direct():
    # Test if we can reach the Go backend directly
    url = "http://127.0.0.1:9090/api"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8')
            assert "Go Backend Online" in body, f"Expected 'Go Backend Online' from {url}, got '{body}'"
    except Exception as e:
        assert False, f"Failed to connect to Go backend at {url} or received an error: {e}"