# test_final_state.py

import os
import subprocess
import time
import socket
import requests
import re
import smtplib

def test_01_deploy_and_services():
    assert os.path.isfile("/app/deploy.sh"), "/app/deploy.sh does not exist"

    # Run deploy.sh
    result = subprocess.run(["bash", "/app/deploy.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy.sh failed with exit code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    # Wait for services to start
    time.sleep(2)

    # Check if ports 8080 and 2525 are open
    for port in [8080, 2525]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            assert s.connect_ex(('127.0.0.1', port)) == 0, f"Service is not listening on port {port}"

def test_02_fstab_optimized():
    fstab_path = "/app/fstab.optimized"
    assert os.path.isfile(fstab_path), f"{fstab_path} is missing"

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    # Standard fstab format entry to mount /dev/sdb1 to /mnt/cold_archive using ext4
    # options: noatime,nodiratime,ro
    # dump/pass: 0 2
    pattern = r"^/dev/sdb1\s+/mnt/cold_archive\s+ext4\s+noatime,nodiratime,ro\s+0\s+2$"
    assert re.search(pattern, content, re.MULTILINE), f"fstab.optimized content does not match expected format. Got: {content}"

def test_03_symlinks():
    links = {
        "bucket_alpha": "/app/raw_data/us-east-1",
        "bucket_beta": "/app/raw_data/eu-west-1",
        "bucket_gamma": "/app/raw_data/ap-south-1"
    }

    for link_name, target in links.items():
        link_path = os.path.join("/app/data_links", link_name)
        assert os.path.islink(link_path), f"{link_path} is not a symlink"
        assert os.readlink(link_path) == target, f"Symlink {link_path} points to {os.readlink(link_path)}, expected {target}"

def test_04_http_unauthorized():
    url = "http://127.0.0.1:8080/cost?bucket=bucket_alpha"
    response = requests.get(url)
    assert response.status_code == 401, f"Expected HTTP 401 for unauthenticated request, got {response.status_code}"

def test_05_http_authorized_cost():
    # Create test file of known size in /app/raw_data/us-east-1
    target_dir = "/app/raw_data/us-east-1"
    os.makedirs(target_dir, exist_ok=True)

    # Clear directory first to ensure exact size
    for f in os.listdir(target_dir):
        os.remove(os.path.join(target_dir, f))

    # Write exactly 1500 bytes
    test_file = os.path.join(target_dir, "test.dat")
    with open(test_file, "wb") as f:
        f.write(b"A" * 1500)

    url = "http://127.0.0.1:8080/cost?bucket=bucket_alpha"
    headers = {"Authorization": "Bearer finops_secret_2024"}

    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Body: {response.text}"

    # Expected cost for 1500 bytes: 1000 * 0.05 + 500 * 0.02 = 50 + 10 = 60
    # Expected output string: Cost: $60.00 (or similar float representation)
    # We will just check if 60 is in the string, or run legacy_pricer to get exact string

    # Run legacy_pricer to get exact string
    pricer_result = subprocess.run(["/app/legacy_pricer", "1500"], capture_output=True, text=True)
    expected_cost_val = pricer_result.stdout.strip()

    expected_body = f"Cost: ${expected_cost_val}"
    assert expected_body in response.text or "60" in response.text, f"Expected body to contain {expected_body}, got {response.text}"

def test_06_smtp_alert():
    # Send standard SMTP payload to 127.0.0.1:2525
    sender = "admin@example.com"
    receiver = "finops@example.com"
    subject = "URGENT ALERT OVER BUDGET"
    message = f"Subject: {subject}\r\n\r\nThis is a test message."

    try:
        with smtplib.SMTP("127.0.0.1", 2525, timeout=5) as server:
            server.sendmail(sender, receiver, message)
    except Exception as e:
        assert False, f"Failed to send SMTP message: {e}"

    time.sleep(1) # Wait for log to be written

    log_path = "/app/alerts.log"
    assert os.path.isfile(log_path), f"Alerts log {log_path} was not created"

    with open(log_path, "r") as f:
        content = f.read()

    assert subject in content, f"Expected subject '{subject}' not found in {log_path}. Content: {content}"