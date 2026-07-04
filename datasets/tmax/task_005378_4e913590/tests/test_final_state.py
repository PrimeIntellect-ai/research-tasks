# test_final_state.py
import os
import subprocess
import json
import pytest

def test_mock_fstab_updated():
    fstab_path = '/home/user/mock_fstab'
    assert os.path.exists(fstab_path), f"{fstab_path} does not exist"
    with open(fstab_path, 'r') as f:
        content = f.read()
    expected_line = '/home/user/storage.img /home/user/app_root/storage ext4 defaults 0 2'
    assert expected_line in content, f"Expected line '{expected_line}' not found in {fstab_path}"

def test_crontab_updated():
    try:
        cron_output = subprocess.check_output(['crontab', '-l'], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        cron_output = e.output

    expected_cron = '*/5 * * * * /usr/bin/python3 /home/user/app_root/healthcheck.py >> /home/user/health.log 2>&1'
    assert expected_cron in cron_output, "Expected crontab entry not found in crontab -l"

def test_files_extracted():
    server_py = '/home/user/app_root/server.py'
    healthcheck_py = '/home/user/app_root/healthcheck.py'
    assert os.path.isfile(server_py), f"Extracted file {server_py} does not exist"
    assert os.path.isfile(healthcheck_py), f"Extracted file {healthcheck_py} does not exist"

def test_server_running_and_pid_file():
    pid_file = '/home/user/app_root/server.pid'
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist"

    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID"
    pid = int(pid_str)

    cmdline_file = f'/proc/{pid}/cmdline'
    assert os.path.exists(cmdline_file), f"Process with PID {pid} is not running (no {cmdline_file})"

    with open(cmdline_file, 'r') as f:
        cmdline = f.read()

    assert 'server.py' in cmdline, f"Process {pid} is running but its cmdline does not contain 'server.py'"