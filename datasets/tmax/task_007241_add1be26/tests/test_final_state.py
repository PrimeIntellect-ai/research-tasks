# test_final_state.py
import os
import subprocess
import urllib.request
import ssl
import time
import socket

def test_nginx_config_fixed():
    nginx_conf = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf), f"Nginx config {nginx_conf} is missing."
    with open(nginx_conf, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:9000;" in content, "Nginx config was not updated to proxy to port 9000."

def test_tls_certificates_exist_and_valid():
    cert_file = "/home/user/nginx/certs/server.crt"
    key_file = "/home/user/nginx/certs/server.key"
    assert os.path.isfile(cert_file), f"Certificate file {cert_file} is missing."
    assert os.path.isfile(key_file), f"Key file {key_file} is missing."

    # Check if they are valid using openssl
    cert_check = subprocess.run(["openssl", "x509", "-in", cert_file, "-text", "-noout"], capture_output=True)
    assert cert_check.returncode == 0, f"Certificate {cert_file} is not a valid X509 certificate."

    key_check = subprocess.run(["openssl", "rsa", "-in", key_file, "-check", "-noout"], capture_output=True)
    assert key_check.returncode == 0, f"Key {key_file} is not a valid RSA key."

def test_expect_script_exists_and_works():
    expect_script = "/home/user/test_smtp.exp"
    assert os.path.isfile(expect_script), f"Expect script {expect_script} is missing."

    # Start a mock SMTP server
    smtp_proc = subprocess.Popen(["python3", "-m", "smtpd", "-n", "-c", "DebuggingServer", "127.0.0.1:2525"])
    time.sleep(1) # wait for server to start

    try:
        # Run the expect script
        result = subprocess.run(["expect", expect_script], capture_output=True, text=True)
        assert result.returncode == 0, f"Expect script failed to execute properly. Output: {result.stdout}\n{result.stderr}"
    finally:
        smtp_proc.terminate()
        smtp_proc.wait()

def test_endpoint_accessibility():
    # The services should be running if start_all.sh was executed properly.
    # We can check the endpoint directly.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:8443/status"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            assert body == "OK", f"Expected body 'OK', got '{body}'"
    except Exception as e:
        pytest.fail(f"Failed to access {url}: {e}")

def test_result_log():
    result_log = "/home/user/result.log"
    assert os.path.isfile(result_log), f"Result log {result_log} is missing."
    with open(result_log, "r") as f:
        content = f.read().strip()
    assert "200" in content, f"Expected '200' in {result_log}, got '{content}'"