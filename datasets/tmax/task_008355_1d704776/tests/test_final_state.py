# test_final_state.py

import os
import glob
import gzip
import subprocess

def test_directories_exist():
    """Check that logs and backups directories exist."""
    assert os.path.isdir('/home/user/logs'), "/home/user/logs directory does not exist."
    assert os.path.isdir('/home/user/backups'), "/home/user/backups directory does not exist."

def test_c_program_and_binary_exist():
    """Check that the C source code and executable binary exist."""
    assert os.path.isfile('/home/user/disk_monitor.c'), "disk_monitor.c does not exist."
    assert os.path.isfile('/home/user/disk_monitor'), "disk_monitor binary does not exist."
    assert os.access('/home/user/disk_monitor', os.X_OK), "disk_monitor is not executable."

def test_backup_script_exists_and_executable():
    """Check that the backup script exists and is executable."""
    assert os.path.isfile('/home/user/backup.sh'), "backup.sh does not exist."
    assert os.access('/home/user/backup.sh', os.X_OK), "backup.sh is not executable."

def test_logrotate_conf_exists():
    """Check that the logrotate configuration file exists."""
    assert os.path.isfile('/home/user/logrotate.conf'), "logrotate.conf does not exist."

def test_vm_disk_size():
    """Verify that the VM disk is exactly 20 Megabytes (20971520 bytes)."""
    disk_path = '/home/user/vm_disk.img'
    assert os.path.isfile(disk_path), f"{disk_path} does not exist."

    # We can check the actual file size as qemu-img raw files report their size to stat
    size = os.path.getsize(disk_path)
    assert size == 20971520, f"Expected VM disk size to be 20971520 bytes, got {size} bytes."

def test_backups_created():
    """Verify that at least one backup was created and no more than 3 exist."""
    backups = glob.glob('/home/user/backups/vm_disk_backup_*.img')
    assert len(backups) >= 1, "No backup files found in /home/user/backups/."
    assert len(backups) <= 3, f"Found {len(backups)} backups, but expected at most 3."

def test_log_rotation_and_contents():
    """Verify that the log was rotated and contains the correct threshold message."""
    log_files = glob.glob('/home/user/logs/monitor.log*')
    assert len(log_files) > 0, "No monitor.log files found in /home/user/logs/."

    # Check if rotated log exists (either compressed or uncompressed)
    rotated_logs = [f for f in log_files if f != '/home/user/logs/monitor.log']
    assert len(rotated_logs) > 0, "Log file was not rotated. Expected monitor.log.1 or monitor.log.1.gz to exist."

    expected_message = "THRESHOLD_EXCEEDED: 20971520"
    message_found = False

    for log_file in log_files:
        try:
            if log_file.endswith('.gz'):
                with gzip.open(log_file, 'rt') as f:
                    content = f.read()
            else:
                with open(log_file, 'r') as f:
                    content = f.read()

            if expected_message in content:
                message_found = True
                break
        except Exception:
            pass

    assert message_found, f"Expected log message '{expected_message}' not found in any log files."