# test_final_state.py

import os
import subprocess
import urllib.request
import ssl
import time

def test_files_exist():
    """Test that all required files have been created."""
    required_files = [
        "/home/user/certs/cert.pem",
        "/home/user/certs/key.pem",
        "/home/user/tls_proxy.py",
        "/home/user/supervisord.conf",
        "/home/user/cicd_restore.py"
    ]
    for filepath in required_files:
        assert os.path.isfile(filepath), f"Required file {filepath} does not exist."

def test_supervisord_running():
    """Test that supervisord is running."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "supervisord"], text=True)
        assert output.strip(), "supervisord is not running."
    except subprocess.CalledProcessError:
        assert False, "supervisord is not running."

def test_cicd_restore_and_proxy():
    """Test the CI/CD script with v2 backup and verify the proxy response."""
    script_path = "/home/user/cicd_restore.py"
    backup_path = "/home/user/archive/v2.tar.gz"
    log_path = "/home/user/restore_log.txt"

    # Run the CI/CD script
    try:
        subprocess.run(
            ["python3", script_path, backup_path],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        assert False, f"CI/CD script failed to run: {e.stderr}"

    # Give it a small buffer just in case
    time.sleep(1)

    # Check the log file
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."
    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()
        assert len(lines) > 0, "Log file is empty."
        assert "APP_VERSION_2_RESTORED" in lines[-1], "The last line of the log file does not contain the expected response."

    # Check the proxy directly
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://127.0.0.1:8443/")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            body = response.read().decode("utf-8")
            assert "APP_VERSION_2_RESTORED" in body, f"Proxy returned unexpected response: {body}"
    except Exception as e:
        assert False, f"Failed to connect to the TLS proxy or verify response: {e}"