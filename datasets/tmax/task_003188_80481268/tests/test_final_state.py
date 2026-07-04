# test_final_state.py

import os
import stat
import socket
import subprocess
import time
import pytest

def test_systemd_service_configured_and_running():
    """Check if the systemd service is configured properly and is active."""
    service_file = "/home/user/.config/systemd/user/exporter.service"
    assert os.path.isfile(service_file), f"Service file {service_file} does not exist."

    with open(service_file, "r") as f:
        content = f.read()

    assert "Restart=always" in content, "Service file missing Restart=always"
    assert "RestartSec=2" in content, "Service file missing RestartSec=2"
    assert "/home/user/bin/exporter" in content, "Service file does not execute the correct binary path"

    result = subprocess.run(["systemctl", "--user", "is-active", "exporter.service"], capture_output=True, text=True)
    assert result.stdout.strip() == "active", f"Service is not active. Status: {result.stdout.strip()}"

def test_deploy_script_behavior():
    """Check if the deployment script works as specified."""
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"Deploy script {deploy_script} does not exist."
    assert os.stat(deploy_script).st_mode & stat.S_IXUSR, f"Deploy script {deploy_script} is not executable."

    test_version = "v1.5-test"
    result = subprocess.run([deploy_script, test_version], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy.sh failed to execute. Error: {result.stderr}"

    version_file = "/home/user/version.txt"
    assert os.path.isfile(version_file), f"Version file {version_file} was not created."

    with open(version_file, "r") as f:
        written_version = f.read().strip()

    assert written_version == test_version, f"Expected version '{test_version}' in version.txt, got '{written_version}'"

    # Wait briefly and check if the service is still active
    time.sleep(1)
    result = subprocess.run(["systemctl", "--user", "is-active", "exporter.service"], capture_output=True, text=True)
    assert result.stdout.strip() == "active", "Service is not active after running deploy.sh."

def test_throughput_metric():
    """Verify that the service throughput meets the requirement of >= 1000 requests per second."""
    target_ip = "127.0.0.1"
    target_port = 8080
    request = b"GET /metrics HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"

    start_time = time.time()
    count = 0
    duration = 2.0  # test for 2 seconds

    while time.time() - start_time < duration:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((target_ip, target_port))
            s.sendall(request)
            data = s.recv(1024)
            s.close()
            if b"HTTP/1.1 200 OK" in data:
                count += 1
        except Exception:
            pass

    throughput = count / duration
    assert throughput >= 1000, f"Throughput metric failed: achieved {throughput:.2f} rps, expected >= 1000 rps."