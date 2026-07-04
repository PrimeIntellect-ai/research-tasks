# test_final_state.py

import os
import stat
import tarfile
import subprocess
import urllib.request
import ssl
import pytest

def test_directories_and_permissions():
    """Verify directories are created and /home/user/backups has strict permissions."""
    assert os.path.isdir("/home/user/app_data"), "/home/user/app_data does not exist"
    assert os.path.isdir("/home/user/backups"), "/home/user/backups does not exist"
    assert os.path.isdir("/home/user/certs"), "/home/user/certs does not exist"

    st = os.stat("/home/user/backups")
    assert oct(st.st_mode)[-3:] == "700", "/home/user/backups does not have 700 permissions"

def test_config_file():
    """Verify config.txt exists and contains the correct string."""
    config_path = "/home/user/app_data/config.txt"
    assert os.path.isfile(config_path), f"{config_path} does not exist"
    with open(config_path, "r") as f:
        content = f.read()
    assert "db_port=5432" in content, f"{config_path} does not contain 'db_port=5432'"

def test_tls_certificates():
    """Verify TLS cert and key exist and key has strict permissions."""
    cert_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"

    assert os.path.isfile(cert_path), f"{cert_path} does not exist"
    assert os.path.isfile(key_path), f"{key_path} does not exist"

    st = os.stat(key_path)
    assert oct(st.st_mode)[-3:] == "600", f"{key_path} does not have 600 permissions"

def test_c_tool_and_binary():
    """Verify the C source and compiled binary exist."""
    assert os.path.isfile("/home/user/backup_tool.c"), "/home/user/backup_tool.c does not exist"
    assert os.path.isfile("/home/user/backup_tool"), "/home/user/backup_tool does not exist"
    assert os.access("/home/user/backup_tool", os.X_OK), "/home/user/backup_tool is not executable"

def test_backup_archive():
    """Verify the backup archive exists and contains config.txt."""
    archive_path = "/home/user/backups/latest.tar.gz"
    assert os.path.isfile(archive_path), f"{archive_path} does not exist"

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        # The archive might contain 'app_data/config.txt' or 'config.txt' depending on how it was tarred
        assert any("config.txt" in name for name in names), "config.txt not found in the backup archive"

def test_deployment_log():
    """Verify the deployment log has the success message."""
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist"
    with open(log_path, "r") as f:
        content = f.read()
    assert "DEPLOYMENT SUCCESS" in content, "DEPLOYMENT SUCCESS not found in deploy.log"

def test_server_running_and_serving():
    """Verify the openssl server is running on port 8443 and serves the backup archive."""
    # Check if port 8443 is listening
    try:
        output = subprocess.check_output(["ss", "-tlnp"], text=True)
        assert ":8443" in output, "Server is not listening on port 8443"
    except FileNotFoundError:
        # Fallback if ss is not available
        pass

    # Download the file via HTTPS
    url = "https://127.0.0.1:8443/latest.tar.gz"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = response.read()
            assert len(data) > 0, "Downloaded file is empty"
    except Exception as e:
        pytest.fail(f"Failed to download the backup archive from the secure server: {e}")