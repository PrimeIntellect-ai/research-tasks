# test_final_state.py
import os
import re
import pytest

def test_backup_exists_and_correct():
    backup_path = "/home/user/backup/nginx.conf.bak"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

    with open(backup_path, "r") as f:
        content = f.read()

    assert "127.0.0.1:8082" in content, "Backup file does not contain the original broken proxy_pass port (8082)."

def test_bashrc_backend_port_exported():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."

    with open(bashrc_path, "r") as f:
        content = f.read()

    # Strip quotes to handle both export BACKEND_PORT=8081 and export BACKEND_PORT="8081"
    normalized_content = content.replace('"', '').replace("'", "")
    assert re.search(r'export\s+BACKEND_PORT=8081\b', normalized_content), "BACKEND_PORT=8081 is not correctly exported in .bashrc."

def test_nginx_config_fixed():
    config_path = "/home/user/nginx_setup/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config {config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert "127.0.0.1:8081" in content, "Nginx config does not contain the corrected proxy_pass port (8081)."

def test_monitor_script_and_status_log():
    monitor_path = "/home/user/monitor.sh"
    status_path = "/home/user/status.log"

    assert os.path.isfile(monitor_path), f"Monitor script {monitor_path} does not exist."
    assert os.path.isfile(status_path), f"Status log {status_path} does not exist. Did you run the monitor script?"

    with open(status_path, "r") as f:
        lines = f.read().splitlines()

    assert any(line.strip() == "UP" for line in lines), "status.log does not contain the word 'UP' indicating a successful health check."

def test_port_forward_script():
    script_path = "/home/user/port_forward.sh"
    assert os.path.isfile(script_path), f"Port forward script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "ssh " in content, "The script does not contain an ssh command."
    assert "dev@example.com" in content, "The script does not connect to dev@example.com."

    # Check for required SSH flags (can be separate like -f -N -q or combined like -fNq)
    assert re.search(r'-[a-zA-Z]*f', content) or " -f" in content, "Missing background flag (-f)."
    assert re.search(r'-[a-zA-Z]*N', content) or " -N" in content, "Missing no-command flag (-N)."
    assert re.search(r'-[a-zA-Z]*q', content) or " -q" in content, "Missing quiet flag (-q)."

    # Check for local port forwarding rule
    assert re.search(r'-L\s*8080:[a-zA-Z0-9.\-]+:8080', content), "Missing or incorrect local port forwarding rule (-L 8080:host:8080)."