# test_final_state.py

import os
import tarfile
import socket
import pytest
import requests

def test_end_to_end_backup_flow():
    url = "http://127.0.0.1:8080/backup"
    headers = {
        "Authorization": "Bearer disk-admin-token-99"
    }
    data = "BACKUP /home/user/data/test_vol\n"

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx or request timed out: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "OK", f"Expected response body 'OK', got {repr(response.text)}"

def test_redis_status_updated():
    import socket

    # Simple Redis protocol client
    def redis_command(cmd):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect(('127.0.0.1', 6379))
            sock.sendall(f"{cmd}\r\n".encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
        except Exception as e:
            pytest.fail(f"Failed to communicate with Redis: {e}")
        finally:
            sock.close()
        return response

    response = redis_command("GET backup_status:test_vol")
    assert "COMPLETED" in response, f"Expected Redis key backup_status:test_vol to be 'COMPLETED', got: {response}"

def test_manifest_and_tarball_created():
    manifest_path = "/home/user/archives/test_vol.manifest"
    tarball_path = "/home/user/archives/test_vol.tar.gz"

    assert os.path.exists(manifest_path), f"Manifest file missing at {manifest_path}"
    assert os.path.exists(tarball_path), f"Tarball missing at {tarball_path}"

    with open(manifest_path, "r") as f:
        manifest_content = f.read()

    assert "data.txt" in manifest_content, "data.txt missing from manifest"
    assert "temp.dat" not in manifest_content, "temp.dat should have been excluded but is in manifest"
    assert "ignore.log" not in manifest_content, "ignore.log should have been excluded but is in manifest"

    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            names = tar.getnames()
            # The paths might be relative or absolute depending on the tar invocation, 
            # but we just check if data.txt is in one of the paths
            assert any("data.txt" in name for name in names), "data.txt missing from tarball"
            assert not any("temp.dat" in name for name in names), "temp.dat should not be in tarball"
    except tarfile.TarError as e:
        pytest.fail(f"Failed to read tarball {tarball_path}: {e}")

def test_test_run_log_exists():
    log_path = "/home/user/app/test_run.log"
    assert os.path.exists(log_path), f"Test log file missing at {log_path}"