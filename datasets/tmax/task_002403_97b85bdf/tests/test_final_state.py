# test_final_state.py

import os
import stat
import subprocess
import random
import string
import pytest

def test_waf_script_exists_and_executable():
    waf_path = "/home/user/waf.sh"
    assert os.path.isfile(waf_path), f"{waf_path} does not exist."
    assert os.access(waf_path, os.X_OK), f"{waf_path} is not executable."

def test_var_uploads_permissions():
    uploads_path = "/var/uploads"
    assert os.path.isdir(uploads_path), f"{uploads_path} does not exist."
    st = os.stat(uploads_path)

    # Check permissions 2775
    assert stat.S_IMODE(st.st_mode) == 0o2775, f"Permissions of {uploads_path} are not 2775."

    # Check group ownership
    import grp
    try:
        www_data_gid = grp.getgrnam("www-data").gr_gid
    except KeyError:
        pytest.fail("Group www-data does not exist.")
    assert st.st_gid == www_data_gid, f"Group ownership of {uploads_path} is not www-data."

def test_nginx_conf_updated():
    conf_path = "/app/config/nginx.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "9000" in content, "nginx.conf does not contain the updated port 9000."
    assert "8080" not in content, "nginx.conf still contains the old port 8080."

def test_certificate_validity():
    cert_path = "/app/certs/server.crt"
    assert os.path.isfile(cert_path), f"{cert_path} does not exist."

    # Check if certificate is valid using openssl
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout", "-checkend", "86400"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, "Certificate is expired or invalid."

def generate_http_post(filename, body):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    headers = (
        f"POST /upload HTTP/1.1\r\n"
        f"Host: localhost:8443\r\n"
        f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
    )

    payload = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
        f"Content-Type: text/plain\r\n\r\n"
        f"{body}\r\n"
        f"--{boundary}--\r\n"
    )

    headers += f"Content-Length: {len(payload)}\r\n\r\n"
    return headers + payload

def test_waf_fuzz_equivalence():
    oracle_path = "/app/bin/oracle_waf_reference"
    agent_path = "/home/user/waf.sh"

    assert os.path.isfile(oracle_path), "Oracle program missing."

    random.seed(42)

    malicious_patterns = [
        "../etc/passwd",
        "..%2Fetc/passwd",
        "%2e%2e%2fetc/passwd",
        "/etc/passwd",
        "file.txt\x00.jpg",
        "....//",
        "..\\windows\\system32"
    ]

    benign_chars = string.ascii_letters + string.digits + "_.-"

    N = 100
    for i in range(N):
        is_malicious = random.random() < 0.6
        if is_malicious:
            filename = random.choice(malicious_patterns)
        else:
            length = random.randint(1, 50)
            filename = "".join(random.choice(benign_chars) for _ in range(length))

        body_length = random.randint(10, 1000)
        body = "".join(random.choice(string.ascii_letters) for _ in range(body_length))

        http_request = generate_http_post(filename, body)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=http_request.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        oracle_out = oracle_proc.stdout.decode('utf-8', errors='ignore').strip()
        oracle_code = oracle_proc.returncode

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=http_request.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        agent_out = agent_proc.stdout.decode('utf-8', errors='ignore').strip()
        agent_code = agent_proc.returncode

        assert oracle_code == agent_code, f"Exit code mismatch on input {filename}. Oracle: {oracle_code}, Agent: {agent_code}"
        assert oracle_out == agent_out, f"Output mismatch on input {filename}.\nOracle:\n{oracle_out}\nAgent:\n{agent_out}"