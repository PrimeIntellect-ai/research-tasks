# test_final_state.py

import os
import tarfile
import pytest

def test_backup_archive_exists_and_valid():
    archive_path = "/home/user/backup/data_archive.tar.gz"
    assert os.path.isfile(archive_path), f"Backup archive {archive_path} does not exist."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
            basenames = [os.path.basename(n) for n in names]
            assert "metric1.csv" in basenames, "metric1.csv not found in the backup archive."
            assert "metric2.csv" in basenames, "metric2.csv not found in the backup archive."
    except tarfile.TarError as e:
        pytest.fail(f"Backup archive is not a valid tar.gz file: {e}")

def test_alerts_log_content():
    log_path = "/home/user/alerts.log"
    assert os.path.isfile(log_path), f"Alerts log {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    expected_alert = "ALERT: Worker down. Backup created."
    assert expected_alert in content, f"Expected alert message '{expected_alert}' not found in {log_path}."

def test_worker_running_and_pid_updated():
    pid_file = "/home/user/app.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid numeric PID: '{pid_str}'"
    pid = int(pid_str)

    proc_dir = f"/proc/{pid}"
    assert os.path.isdir(proc_dir), f"Process with PID {pid} is not running."

    cmdline_file = os.path.join(proc_dir, "cmdline")
    assert os.path.isfile(cmdline_file), f"Cannot read cmdline for PID {pid}."

    with open(cmdline_file, "r") as f:
        cmdline = f.read().replace('\x00', ' ')

    assert "worker.py" in cmdline, f"Process {pid} is running, but does not appear to be worker.py. Cmdline: {cmdline}"