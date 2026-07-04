# test_final_state.py

import os
import re
import subprocess
import pytest

def test_deploy_edge_script():
    """Verify deploy_edge.sh exists, is executable, and contains the correct QEMU arguments."""
    script_path = '/home/user/deploy_edge.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'qemu-system-x86_64' in content, "deploy_edge.sh is missing 'qemu-system-x86_64'."
    assert re.search(r'-m\s+512\b', content), "deploy_edge.sh is missing '-m 512'."
    assert '-nographic' in content, "deploy_edge.sh is missing '-nographic'."

    # Check for daemonize or equivalent (task says -nographic and -daemonize or detached)
    # The truth just checks for -nographic, but let's ensure it's there.

    # Check hostfwd 8080 -> 80
    assert re.search(r'hostfwd=[a-zA-Z0-9:]*8080-[a-zA-Z0-9:]*80\b', content) or \
           re.search(r'hostfwd=[a-zA-Z0-9:]*8080::80\b', content) or \
           '8080-:80' in content or '8080::80' in content, \
           "deploy_edge.sh is missing correct hostfwd mapping for port 8080 to 80."

    # Check hostfwd 5901 -> 5900
    assert re.search(r'hostfwd=[a-zA-Z0-9:]*5901-[a-zA-Z0-9:]*5900\b', content) or \
           re.search(r'hostfwd=[a-zA-Z0-9:]*5901::5900\b', content) or \
           '5901-:5900' in content or '5901::5900' in content, \
           "deploy_edge.sh is missing correct hostfwd mapping for port 5901 to 5900."

    assert '/home/user/images/edge_device.img' in content, "deploy_edge.sh does not target the correct image path."

def test_check_quota_script():
    """Verify check_quota.sh exists, is executable, and correctly monitors storage size."""
    script_path = '/home/user/check_quota.sh'
    img_path = '/home/user/images/edge_device.img'
    log_path = '/home/user/alerts.log'

    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Test > 100MB
    size_105mb = 105 * 1024 * 1024
    with open(img_path, 'wb') as f:
        f.seek(size_105mb - 1)
        f.write(b'\0')

    subprocess.run([script_path], check=False)

    assert os.path.isfile(log_path), f"{log_path} was not created."
    with open(log_path, 'r') as f:
        log_content = f.read()

    expected_alert = f"ALERT: Storage limit exceeded - {size_105mb} bytes"
    assert expected_alert in log_content, f"Expected alert '{expected_alert}' not found in {log_path}."

    # Count lines to ensure no extra lines are added when <= 100MB
    lines_before = len(log_content.strip().split('\n'))

    # Test <= 100MB
    size_50mb = 50 * 1024 * 1024
    with open(img_path, 'wb') as f:
        f.seek(size_50mb - 1)
        f.write(b'\0')

    subprocess.run([script_path], check=False)

    with open(log_path, 'r') as f:
        log_content_after = f.read()

    lines_after = len(log_content_after.strip().split('\n'))
    assert lines_before == lines_after, "Script incorrectly added a log entry when size was <= 100MB."

def test_cron_backup():
    """Verify cron_backup.txt contains the correct cron job configuration."""
    backup_path = '/home/user/cron_backup.txt'
    assert os.path.isfile(backup_path), f"{backup_path} does not exist."

    with open(backup_path, 'r') as f:
        content = f.read()

    # Match */15 or 0,15,30,45
    has_schedule = re.search(r'(?:\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*', content)
    has_script = '/home/user/check_quota.sh' in content

    assert has_schedule and has_script, f"cron_backup.txt does not contain the correct 15-minute schedule for check_quota.sh. Found: {content}"