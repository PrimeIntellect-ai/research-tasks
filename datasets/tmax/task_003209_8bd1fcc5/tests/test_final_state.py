# test_final_state.py

import os
import json
import re
import socket
import ssl
import tarfile
import urllib.request
from pathlib import Path

def test_qemu_process():
    pid_file = Path("/home/user/qemu.pid")
    assert pid_file.exists(), "QEMU PID file /home/user/qemu.pid does not exist."

    pid = pid_file.read_text().strip()
    assert pid.isdigit(), f"PID file does not contain a valid integer: {pid}"

    comm_file = Path(f"/proc/{pid}/comm")
    assert comm_file.exists(), f"Process with PID {pid} is not running."

    comm = comm_file.read_text().strip()
    assert "qemu-system-x86" in comm, f"Process {pid} is not qemu-system-x86_64 (found {comm})."

    # Check if VNC is listening on 127.0.0.1:5905
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', 5905))
    sock.close()
    assert result == 0, "QEMU is not listening on 127.0.0.1:5905."

def test_cpp_analyzer():
    cpp_file = Path("/home/user/capacity_planner/analyzer.cpp")
    bin_file = Path("/home/user/capacity_planner/analyzer")
    assert cpp_file.exists(), "/home/user/capacity_planner/analyzer.cpp does not exist."
    assert bin_file.exists() and os.access(bin_file, os.X_OK), "/home/user/capacity_planner/analyzer is missing or not executable."

    bash_profile = Path("/home/user/.bash_profile")
    assert bash_profile.exists(), "/home/user/.bash_profile does not exist."
    content = bash_profile.read_text()
    assert "export METRICS_FILE=/home/user/metrics/current.json" in content, "METRICS_FILE export is missing in .bash_profile."

    metrics_file = Path("/home/user/metrics/current.json")
    assert metrics_file.exists(), "/home/user/metrics/current.json does not exist."

    metrics_content = metrics_file.read_text().strip()
    assert re.match(r'^\{"vmem_pages"\s*:\s*\d+\}$', metrics_content), f"Metrics file content does not match expected JSON format: {metrics_content}"

def test_nginx_tls():
    cert_file = Path("/home/user/tls/cert.pem")
    key_file = Path("/home/user/tls/key.pem")
    assert cert_file.exists(), "/home/user/tls/cert.pem does not exist."
    assert key_file.exists(), "/home/user/tls/key.pem does not exist."

    nginx_conf = Path("/home/user/nginx.conf")
    assert nginx_conf.exists(), "/home/user/nginx.conf does not exist."

    # Check if Nginx is serving the file over HTTPS
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.urlopen("https://127.0.0.1:8443/current.json", context=ctx, timeout=5)
        assert req.getcode() == 200, f"Expected HTTP 200, got {req.getcode()}"
        body = req.read().decode('utf-8').strip()
        assert re.match(r'^\{"vmem_pages"\s*:\s*\d+\}$', body), "Served JSON does not match expected format."
    except Exception as e:
        pytest.fail(f"Failed to fetch metrics from Nginx over HTTPS: {e}")

def test_backup():
    backup_file = Path("/home/user/backups/metrics_backup.tar.gz")
    assert backup_file.exists(), "Backup tarball /home/user/backups/metrics_backup.tar.gz does not exist."

    assert tarfile.is_tarfile(backup_file), "Backup file is not a valid tar archive."

    with tarfile.open(backup_file, "r:gz") as tar:
        names = tar.getnames()
        # The file can be stored as home/user/metrics/current.json or current.json etc.
        found = any("current.json" in name for name in names)
        assert found, "current.json not found inside the backup tarball."

        for member in tar.getmembers():
            if "current.json" in member.name:
                f = tar.extractfile(member)
                assert f is not None, "Could not extract current.json from tarball."
                content = f.read().decode('utf-8').strip()
                assert re.match(r'^\{"vmem_pages"\s*:\s*\d+\}$', content), "JSON inside backup tarball is invalid."
                break