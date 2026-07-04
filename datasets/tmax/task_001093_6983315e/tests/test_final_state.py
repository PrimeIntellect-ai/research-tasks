# test_final_state.py

import os
import tarfile
import socket
import pytest
import requests

def test_system_conf_updated():
    """Verify that /home/user/system.conf exists and has the updated values."""
    conf_path = "/home/user/system.conf"
    assert os.path.isfile(conf_path), f"Missing updated config file at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "max_worker_threads=1024" in content, "max_worker_threads not updated correctly in system.conf"
    assert "cache_retention_days=30" in content, "cache_retention_days not updated correctly in system.conf"
    assert "log_level=warn" in content, "log_level not updated correctly in system.conf"
    assert "database_url=postgres://localhost:5432" in content, "database_url missing or altered in system.conf"

def test_archive_updated():
    """Verify that the configuration archive exists and contains the updated system.conf."""
    archive_path = "/home/user/config_archive.tar.gz"
    assert os.path.isfile(archive_path), f"Missing config archive at {archive_path}"

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()
        assert "system.conf" in members, "Archive does not contain 'system.conf'"

        f = tar.extractfile("system.conf")
        assert f is not None, "Could not extract 'system.conf' from archive"

        content = f.read().decode("utf-8")

        assert "max_worker_threads=1024" in content, "max_worker_threads not updated correctly in archived system.conf"
        assert "cache_retention_days=30" in content, "cache_retention_days not updated correctly in archived system.conf"
        assert "log_level=warn" in content, "log_level not updated correctly in archived system.conf"
        assert "database_url=postgres://localhost:5432" in content, "database_url missing or altered in archived system.conf"

def test_http_server_port_9000():
    """Verify HTTP server on port 9000 serves the correct configuration values."""
    try:
        r1 = requests.get("http://localhost:9000/get?key=max_worker_threads", timeout=2)
        assert r1.status_code == 200, f"Expected HTTP 200, got {r1.status_code}"
        assert r1.text.strip() == "1024", f"Expected '1024', got '{r1.text}'"

        r2 = requests.get("http://localhost:9000/get?key=cache_retention_days", timeout=2)
        assert r2.status_code == 200, f"Expected HTTP 200, got {r2.status_code}"
        assert r2.text.strip() == "30", f"Expected '30', got '{r2.text}'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request to port 9000 failed: {e}")

def test_tcp_server_port_9001():
    """Verify raw TCP server on port 9001 serves the correct configuration values."""
    def query_tcp(key):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect(("localhost", 9001))
            s.sendall(f"{key}\n".encode("utf-8"))
            response = s.recv(1024).decode("utf-8")
            s.close()
            return response
        except Exception as e:
            pytest.fail(f"TCP request to port 9001 failed for key '{key}': {e}")

    resp1 = query_tcp("log_level")
    assert resp1.strip() == "warn", f"Expected 'warn', got '{resp1.strip()}'"

    resp2 = query_tcp("database_url")
    assert resp2.strip() == "postgres://localhost:5432", f"Expected 'postgres://localhost:5432', got '{resp2.strip()}'"