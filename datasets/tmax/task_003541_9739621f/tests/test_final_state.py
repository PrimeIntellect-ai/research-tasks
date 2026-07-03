# test_final_state.py

import os
import tarfile
import stat
import requests
import pytest

def test_http_status_and_auth_ok():
    """
    Connect to Nginx on 127.0.0.1:8080/status to verify the proxy is working,
    the backend is running, and the correct auth token was generated.
    """
    url = "http://127.0.0.1:8080/status"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}. Is Nginx running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"
    assert "AUTH_OK" in response.text, f"Expected 'AUTH_OK' in response body, but it was missing. Response body: {response.text}"

def test_backup_tarball_exists_and_valid():
    """
    Verify that the backup tarball exists and is a valid gzip-compressed tar archive.
    """
    backup_path = "/app/backup/backend_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."
    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            members = tar.getnames()
            assert len(members) > 0, "Tar archive is empty."
            # Ensure at least one file from the backend directory is in the backup
            assert any("server.py" in member or "init.sh" in member for member in members), "Backup does not seem to contain the backend files."
    except tarfile.TarError as e:
        pytest.fail(f"Backup file {backup_path} is not a valid gzip-compressed tarball: {e}")

def test_socket_permissions():
    """
    Verify that the Unix socket exists, is a socket, and has 666 permissions.
    """
    socket_path = "/app/run/app_backend.sock"
    assert os.path.exists(socket_path), f"Socket file {socket_path} does not exist. Did the backend start?"

    file_stat = os.stat(socket_path)
    assert stat.S_ISSOCK(file_stat.st_mode), f"{socket_path} is not a Unix socket."

    # Check if permissions are exactly 666 (rw-rw-rw-)
    permissions = file_stat.st_mode & 0o777
    assert permissions == 0o666, f"Expected socket permissions to be 666, but got {oct(permissions)}."

def test_nginx_config_updated():
    """
    Verify that the Nginx configuration file was updated with the correct socket path.
    """
    config_path = "/app/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config {config_path} does not exist."
    with open(config_path, "r") as f:
        content = f.read()

    assert "wrong.sock" not in content, "Nginx config still contains the broken 'wrong.sock' path."
    assert "/app/run/app_backend.sock" in content, "Nginx config does not contain the correct socket path (/app/run/app_backend.sock)."