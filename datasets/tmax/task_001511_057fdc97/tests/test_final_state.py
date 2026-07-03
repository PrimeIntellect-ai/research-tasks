# test_final_state.py

import os
import subprocess
import glob
import time
import shutil

def test_monitor_compiled_and_runs():
    binary_path = "/home/user/app/bin/monitor"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

    # Run the binary to ensure it doesn't segfault
    try:
        result = subprocess.run([binary_path], capture_output=True, timeout=5)
        assert result.returncode == 0, f"Binary exited with non-zero code: {result.returncode}"
    except Exception as e:
        pytest.fail(f"Failed to run the monitor binary: {e}")

    log_path = "/home/user/app/logs/monitor.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created by the monitor program."

def test_backup_script():
    script_path = "/home/user/app/scripts/backup.sh"
    assert os.path.isfile(script_path), f"Backup script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Backup script {script_path} is not executable."

    # Count existing backups
    backup_dir = "/home/user/backups"
    os.makedirs(backup_dir, exist_ok=True)
    initial_backups = set(glob.glob(os.path.join(backup_dir, "data_backup_*.tar.gz")))

    # Run the backup script
    result = subprocess.run([script_path], capture_output=True, timeout=10)
    assert result.returncode == 0, f"Backup script failed with exit code {result.returncode}"

    # Check for new backup
    current_backups = set(glob.glob(os.path.join(backup_dir, "data_backup_*.tar.gz")))
    new_backups = current_backups - initial_backups
    assert len(new_backups) >= 1, "Backup script did not create a new data_backup_<timestamp>.tar.gz file."

def test_restore_script():
    script_path = "/home/user/app/scripts/restore.sh"
    assert os.path.isfile(script_path), f"Restore script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Restore script {script_path} is not executable."

    data_dir = "/home/user/data"
    backup_dir = "/home/user/backups"

    # Ensure there is at least one backup to restore from
    backups = glob.glob(os.path.join(backup_dir, "data_backup_*.tar.gz"))
    if not backups:
        # Run backup script to create one if none exist
        subprocess.run(["/home/user/app/scripts/backup.sh"], check=True)
        backups = glob.glob(os.path.join(backup_dir, "data_backup_*.tar.gz"))

    latest_backup = max(backups, key=os.path.getctime)

    # Modify data dir to test restore
    test_file = os.path.join(data_dir, "test_restore_marker.txt")
    with open(test_file, "w") as f:
        f.write("marker")

    # Run restore script
    result = subprocess.run([script_path, latest_backup], capture_output=True, timeout=10)
    assert result.returncode == 0, f"Restore script failed with exit code {result.returncode}"

    # Check that marker is gone (directory was cleared before extract)
    assert not os.path.exists(test_file), "Restore script did not clear the data directory before extracting."

    # Check that original files are present
    assert os.path.isfile(os.path.join(data_dir, "file1.txt")), "Restored data is missing file1.txt"
    assert os.path.isfile(os.path.join(data_dir, "file2.txt")), "Restored data is missing file2.txt"

def test_crontab_configured():
    # Check crontab for the user
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    # It might fail if no crontab for user, but task requires it
    assert result.returncode == 0, "No crontab found for user."

    crontab_content = result.stdout
    assert "backup.sh" in crontab_content, "backup.sh not found in crontab."

    # Look for the schedule "0 * * * *"
    found_schedule = False
    for line in crontab_content.splitlines():
        if not line.strip().startswith("#") and "backup.sh" in line:
            parts = line.split()
            if len(parts) >= 5:
                schedule = " ".join(parts[:5])
                if schedule == "0 * * * *":
                    found_schedule = True
                    break

    assert found_schedule, "Crontab does not have the correct schedule (0 * * * *) for backup.sh."

def test_logrotate_config():
    config_path = "/home/user/app/config/logrotate.conf"
    assert os.path.isfile(config_path), f"Logrotate config {config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert "/home/user/app/logs/monitor.log" in content, "Logrotate config does not target /home/user/app/logs/monitor.log"
    assert "daily" in content, "Logrotate config missing 'daily'"
    assert "rotate 3" in content, "Logrotate config missing 'rotate 3'"
    assert "compress" in content, "Logrotate config missing 'compress'"
    assert "missingok" in content, "Logrotate config missing 'missingok'"