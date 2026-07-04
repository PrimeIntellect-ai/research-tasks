# test_final_state.py

import os
import stat
import subprocess
import time
import urllib.request
import ssl
import pytest

def test_bashrc_env_vars():
    """Check that BACKEND_A and BACKEND_B are defined in .bashrc."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert "BACKEND_A=9001" in content.replace("export ", "").replace('"', '').replace("'", ""), "BACKEND_A=9001 not found in .bashrc"
    assert "BACKEND_B=9002" in content.replace("export ", "").replace('"', '').replace("'", ""), "BACKEND_B=9002 not found in .bashrc"

def test_ssl_cert_and_key():
    """Check that the SSL certificate and key exist."""
    cert_path = "/home/user/ssl/server.crt"
    key_path = "/home/user/ssl/server.key"

    assert os.path.isfile(cert_path), f"Certificate not found at {cert_path}"
    assert os.path.isfile(key_path), f"Key not found at {key_path}"

def test_backends_script():
    """Check that backends.sh exists and is executable."""
    script_path = "/home/user/backends.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable by the user."

def test_nginx_conf():
    """Check that nginx.conf exists and contains required directives."""
    conf_path = "/home/user/nginx/conf/nginx.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "8443" in content, "Nginx does not appear to be configured to listen on port 8443."
    assert "ssl" in content.lower(), "Nginx does not appear to have SSL enabled."
    assert "client_body_temp_path" in content, "client_body_temp_path directive is missing."
    assert "proxy_temp_path" in content, "proxy_temp_path directive is missing."
    assert "fastcgi_temp_path" in content, "fastcgi_temp_path directive is missing."
    assert "uwsgi_temp_path" in content, "uwsgi_temp_path directive is missing."
    assert "scgi_temp_path" in content, "scgi_temp_path directive is missing."
    assert "user " not in content, "The 'user' directive should be omitted for unprivileged execution."

def test_start_all_script():
    """Check that start_all.sh exists and is executable."""
    script_path = "/home/user/start_all.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable by the user."

def test_integration():
    """Run start_all.sh and verify round-robin load balancing over HTTPS."""
    # Ensure any previous instances are stopped
    subprocess.run(["pkill", "-f", "nginx"], stderr=subprocess.DEVNULL)

    # Run the start script
    start_cmd = "source /home/user/.bashrc && /home/user/start_all.sh"
    result = subprocess.run(start_cmd, shell=True, executable="/bin/bash")
    assert result.returncode == 0, "start_all.sh failed to execute successfully."

    # Give the servers a moment to start
    time.sleep(2)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req1 = urllib.request.urlopen("https://localhost:8443/", context=ctx, timeout=5)
        resp1 = req1.read().decode('utf-8')

        req2 = urllib.request.urlopen("https://localhost:8443/", context=ctx, timeout=5)
        resp2 = req2.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx on port 8443: {e}")

    has_a = "Backend A" in resp1 or "Backend A" in resp2
    has_b = "Backend B" in resp1 or "Backend B" in resp2

    assert has_a and has_b, f"Did not receive responses from both backends. Resp1: {resp1.strip()}, Resp2: {resp2.strip()}"