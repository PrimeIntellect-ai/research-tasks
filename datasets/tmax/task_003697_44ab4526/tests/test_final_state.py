# test_final_state.py

import os
import re
import socket
import subprocess
import pytest

def test_deploy_script_exists():
    path = "/home/user/deploy_restore_test.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "#!/bin/" in content or "bash" in content, f"File {path} does not appear to be a valid bash script."

def test_restore_env_file():
    path = "/home/user/restore_env.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert re.search(r"export\s+DB_PORT=9091", content), "DB_PORT=9091 not exported correctly in restore_env.sh"
    assert re.search(r"export\s+RESTORE_ENV=testing", content), "RESTORE_ENV=testing not exported correctly in restore_env.sh"

def test_service_pids_file():
    path = "/home/user/service.pids"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 3, f"Expected exactly 3 PIDs in {path}, found {len(lines)}"
    for pid in lines:
        assert pid.isdigit(), f"Found non-integer PID '{pid}' in {path}"

def test_logrotate_conf():
    path = "/home/user/logrotate.conf"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "size 10k" in content, "Missing 'size 10k' in logrotate.conf"
    assert "rotate 5" in content, "Missing 'rotate 5' in logrotate.conf"
    assert "compress" in content, "Missing 'compress' in logrotate.conf"
    assert "missingok" in content, "Missing 'missingok' in logrotate.conf"
    assert "/home/user/logs/*.log" in content or "/home/user/logs/" in content, "Target log path not found in logrotate.conf"

def test_logrotate_state():
    path = "/home/user/logrotate.state"
    assert os.path.isfile(path), f"File {path} does not exist (logrotate might not have been executed with custom state file)."
    with open(path, "r") as f:
        content = f.read()
    assert "db.log" in content, "db.log not found in logrotate.state"
    assert "app.log" in content, "app.log not found in logrotate.state"

def test_processes_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps aux")

    assert "db-restore.sh" in output, "db-restore.sh process is not running."
    assert "app-restore.sh" in output, "app-restore.sh process is not running."
    assert "-L 9091:127.0.0.1:8081" in output or "-L 127.0.0.1:9091:127.0.0.1:8081" in output, "SSH tunnel process with correct port forwarding is not running."

def test_network_tunnel():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', 9091))
    sock.close()
    assert result == 0, "Cannot connect to 127.0.0.1:9091. The SSH tunnel might not be working or db-restore.sh is not listening on 8081."

def test_log_rotation_executed():
    db_gz = "/home/user/logs/db.log.1.gz"
    app_gz = "/home/user/logs/app.log.1.gz"
    assert os.path.isfile(db_gz), f"Rotated log {db_gz} does not exist. Logrotate may not have run or compressed the files."
    assert os.path.isfile(app_gz), f"Rotated log {app_gz} does not exist. Logrotate may not have run or compressed the files."