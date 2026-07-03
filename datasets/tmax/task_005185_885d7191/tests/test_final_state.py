# test_final_state.py

import os
import subprocess
import re
import pytest

def test_scripts_exist_and_executable():
    check_storage = "/home/user/check_storage.sh"
    assert os.path.isfile(check_storage), f"{check_storage} is missing"
    assert os.access(check_storage, os.X_OK), f"{check_storage} is not executable"

    edge_daemon = "/home/user/edge_daemon.sh"
    assert os.path.isfile(edge_daemon), f"{edge_daemon} is missing"
    assert os.access(edge_daemon, os.X_OK), f"{edge_daemon} is not executable"

def test_logrotate_conf_exists_and_contains_rules():
    conf_path = "/home/user/iot_logrotate.conf"
    assert os.path.isfile(conf_path), f"{conf_path} is missing"

    with open(conf_path, "r") as f:
        content = f.read().lower()

    assert "5m" in content or "5120k" in content, "Size 5M rule not found in logrotate config"
    assert "rotate 2" in content, "rotate 2 rule not found in logrotate config"
    assert "compress" in content, "compress rule not found in logrotate config"
    assert "missingok" in content, "missingok rule not found in logrotate config"
    assert "nomail" in content, "nomail rule not found in logrotate config"

def test_execution_and_results():
    logs_dir = "/home/user/edge_storage/logs"

    # Clean up any existing logs
    for f in os.listdir(logs_dir):
        if f.endswith(".log") or ".log." in f:
            os.remove(os.path.join(logs_dir, f))

    # Create test files with specific sizes to trigger rotation and alerts (6M and 16M)
    subprocess.run(["dd", "if=/dev/urandom", f"of={logs_dir}/sensor_alpha.log", "bs=1M", "count=6"], check=True, stderr=subprocess.DEVNULL)
    subprocess.run(["dd", "if=/dev/urandom", f"of={logs_dir}/sensor_beta.log", "bs=1M", "count=16"], check=True, stderr=subprocess.DEVNULL)

    status_file = "/home/user/logrotate.status"
    if os.path.exists(status_file):
        os.remove(status_file)

    outbox = "/home/user/mail_outbox.log"
    if os.path.exists(outbox):
        os.remove(outbox)

    # Execute daemon
    res = subprocess.run(["/home/user/edge_daemon.sh"], capture_output=True, text=True)
    assert res.returncode == 0, f"edge_daemon.sh failed with output: {res.stderr}"

    # Check logrotate results
    assert os.path.exists(f"{logs_dir}/sensor_alpha.log.1.gz"), "sensor_alpha.log was not rotated and compressed"
    assert os.path.exists(f"{logs_dir}/sensor_beta.log.1.gz"), "sensor_beta.log was not rotated and compressed"

    # Check mail outbox for alert
    assert os.path.exists(outbox), "mail_outbox.log was not created; check_storage.sh failed to send mail."

    with open(outbox, "r") as f:
        mail_content = f.read()

    assert "Subject: ALERT: IoT Storage High" in mail_content, "Missing or incorrect email subject in mail outbox."

    # The total size of the directory should be around 22 MB
    match = re.search(r"Current usage:\s*(\d+)\s*MB", mail_content)
    assert match is not None, "Missing or incorrectly formatted 'Current usage: X MB' string in email body."

    size_mb = int(match.group(1))
    assert size_mb in [21, 22, 23], f"Reported size {size_mb} MB is incorrect (expected ~22 MB)."