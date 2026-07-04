# test_final_state.py
import os
import time
import subprocess
import pytest

def test_provisioning_script_execution_and_speedup():
    provision_script = "/home/user/provision.py"
    assert os.path.exists(provision_script), f"Missing script: {provision_script}"
    assert os.access(provision_script, os.X_OK), f"Script is not executable: {provision_script}"

    start_time = time.time()
    result = subprocess.run(["python3", provision_script], capture_output=True, text=True)
    end_time = time.time()

    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    runtime = end_time - start_time
    reference_time = 20.0
    speedup = reference_time / runtime if runtime > 0 else 0

    assert speedup >= 5.0, f"Speedup too low: {speedup:.2f} (Runtime: {runtime:.2f}s). Expected speedup >= 5.0 (Runtime <= 4.0s)"

def test_generated_files_content():
    # 1. Check create_users.sh
    create_users_path = "/home/user/create_users.sh"
    assert os.path.exists(create_users_path), f"Missing file: {create_users_path}"
    with open(create_users_path, "r") as f:
        create_users_content = f.read()

    for i in range(10):
        expected_cmd = f"useradd -m -s /bin/bash omega_admin_{i}"
        assert expected_cmd in create_users_content, f"Missing expected command in {create_users_path}: {expected_cmd}"

    # 2. Check service_logrotate.conf
    logrotate_path = "/home/user/service_logrotate.conf"
    assert os.path.exists(logrotate_path), f"Missing file: {logrotate_path}"
    with open(logrotate_path, "r") as f:
        logrotate_content = f.read()

    assert "/home/user/logs/service_*.log" in logrotate_content, "Missing target log path in logrotate config"
    assert "daily" in logrotate_content, "Missing 'daily' directive in logrotate config"
    assert "size 100M" in logrotate_content or "size=100M" in logrotate_content.replace(" ", ""), "Missing 'size 100M' directive in logrotate config"
    assert "rotate 7" in logrotate_content, "Missing 'rotate 7' directive in logrotate config"
    assert "missingok" in logrotate_content, "Missing 'missingok' directive in logrotate config"
    assert "compress" in logrotate_content, "Missing 'compress' directive in logrotate config"

    # 3. Check firewall.sh
    firewall_path = "/home/user/firewall.sh"
    assert os.path.exists(firewall_path), f"Missing file: {firewall_path}"
    with open(firewall_path, "r") as f:
        firewall_content = f.read()

    for i in range(10):
        ext_port = 8000 + i
        int_port = 7000 + i
        expected_rule = f"iptables -t nat -A PREROUTING -p tcp --dport {ext_port} -j REDIRECT --to-port {int_port}"
        assert expected_rule in firewall_content, f"Missing expected iptables rule in {firewall_path}: {expected_rule}"

def test_legacy_installer_logs():
    for i in range(10):
        log_path = f"/home/user/logs/service_{i}.log"
        assert os.path.exists(log_path), f"Missing log file: {log_path}"
        with open(log_path, "r") as f:
            log_content = f.read().strip()

        expected_log = f"Provisioned instance {i} for omega_admin_{i} on port {7000 + i}"
        assert expected_log in log_content, f"Incorrect log content in {log_path}. Expected: '{expected_log}', Got: '{log_content}'"