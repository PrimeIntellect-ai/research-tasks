# test_final_state.py

import os
import subprocess
import urllib.request
import ssl
import pytest

def test_symlinks_created():
    """Verify that the directory structure and symlinks are properly created."""
    links = [
        ("2023/01", "cost_report_2023_01.html"),
        ("2023/02", "cost_report_2023_02.html"),
        ("2024/03", "cost_report_2024_03.html"),
    ]

    for path_part, target_file in links:
        link_path = f"/home/user/finops_web/{path_part}/index.html"
        assert os.path.islink(link_path), f"Expected symlink at {link_path} is missing or not a symlink."

        target = os.readlink(link_path)
        abs_target = os.path.normpath(os.path.join(os.path.dirname(link_path), target))
        expected_target = f"/home/user/raw_reports/{target_file}"
        assert abs_target == expected_target, f"Symlink {link_path} points to {abs_target}, expected {expected_target}."

def test_expect_script_exists():
    """Verify the expect script was created."""
    script_path = "/home/user/gen_cert.exp"
    assert os.path.isfile(script_path), f"Expect script {script_path} does not exist."

def test_tls_certificate_details():
    """Verify the TLS certificate exists and has the correct subject details."""
    cert_path = "/home/user/cert.pem"
    key_path = "/home/user/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Key file {key_path} does not exist."

    result = subprocess.run(["openssl", "x509", "-in", cert_path, "-noout", "-subject"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read certificate subject."

    subject = result.stdout
    expected_parts = [
        "C = US",
        "ST = California",
        "L = San Francisco",
        "O = CloudCo",
        "OU = FinOps",
        "CN = localhost",
        "emailAddress = admin@cloudco.local"
    ]

    for part in expected_parts:
        assert part in subject, f"Expected '{part}' in certificate subject, but got: {subject}"

def test_server_script_and_pid():
    """Verify the start_server.sh script exists and the server PID is recorded and running."""
    script_path = "/home/user/start_server.sh"
    pid_path = "/home/user/server.pid"

    assert os.path.isfile(script_path), f"Server script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Server script {script_path} is not executable."

    assert os.path.isfile(pid_path), f"PID file {pid_path} does not exist."

    with open(pid_path, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_path} does not contain a valid integer."

    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

def test_https_server_reachable():
    """Verify the HTTPS server is serving the correct content."""
    url = "https://localhost:8443/2023/01/index.html"

    # Ignore certificate validation since it's self-signed
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(url, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            content = response.read().decode('utf-8')
            assert "Report Jan 2023" in content, "Server did not return the expected content for 2023/01/index.html."
    except Exception as e:
        pytest.fail(f"Failed to fetch {url}: {e}")