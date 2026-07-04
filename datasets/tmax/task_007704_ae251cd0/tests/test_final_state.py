# test_final_state.py

import os
import pytest

def get_directory_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def test_check_quotas_script_exists():
    script_path = "/home/user/check_quotas.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_quota_alerts_log_exists():
    log_path = "/home/user/quota_alerts.log"
    assert os.path.isfile(log_path), f"The log file {log_path} was not created."

def test_quota_alerts_content():
    fstab_path = "/home/user/storage_fstab"
    assert os.path.isfile(fstab_path), f"Missing {fstab_path}"

    expected_alerts = set()
    with open(fstab_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                continue

            symlink_path = parts[0]
            try:
                quota_mb = int(parts[1])
            except ValueError:
                continue

            if not os.path.exists(symlink_path):
                continue

            real_path = os.path.realpath(symlink_path)
            total_bytes = get_directory_size(real_path)
            actual_mb = total_bytes / 1048576.0

            if actual_mb > quota_mb:
                alert_line = f"[ALERT] Symlink: {symlink_path} | RealDir: {real_path} | Quota: {quota_mb}MB | Actual: {actual_mb:.2f}MB"
                expected_alerts.add(alert_line)

    log_path = "/home/user/quota_alerts.log"
    assert os.path.isfile(log_path), f"Missing {log_path}"

    with open(log_path, "r") as f:
        actual_lines = set(line.strip() for line in f if line.strip())

    missing_alerts = expected_alerts - actual_lines
    extra_alerts = actual_lines - expected_alerts

    assert not missing_alerts, f"Missing expected alerts in {log_path}: {missing_alerts}"
    assert not extra_alerts, f"Found unexpected alerts in {log_path}: {extra_alerts}"