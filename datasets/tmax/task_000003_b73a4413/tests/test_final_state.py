# test_final_state.py

import os
import tarfile
import pytest

def test_cpp_source_modified():
    """Test that edge_daemon.cpp was modified to use the correct socket path."""
    file_path = "/home/user/edge_daemon.cpp"
    assert os.path.isfile(file_path), f"Source file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert "/home/user/run/edge.sock" in content, (
        f"File {file_path} does not contain the correct socket path '/home/user/run/edge.sock'."
    )
    assert "/tmp/app.sock" not in content, (
        f"File {file_path} still contains the old incorrect socket path '/tmp/app.sock'."
    )

def test_daemon_compiled():
    """Test that the daemon was compiled into an executable."""
    exe_path = "/home/user/edge_daemon"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_sensor_log_created():
    """Test that the sensor log was generated correctly by the client/daemon interaction."""
    log_path = "/home/user/data/sensor.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did you run the daemon and client script?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "SENSOR_DATA_OK: 42.0" in content, (
        f"File {log_path} does not contain the expected sensor data. Found: {content}"
    )

def test_backup_script_exists():
    """Test that the backup script was created."""
    script_path = "/home/user/backup_job.sh"
    assert os.path.isfile(script_path), f"Backup script {script_path} is missing."

def test_backups_created_and_valid():
    """Test that the three backup tarballs exist, are valid, and contain the sensor log."""
    backup_paths = [
        "/home/user/backups/backup_1.tar.gz",
        "/home/user/backups/backup_2.tar.gz",
        "/home/user/backups/backup_3.tar.gz"
    ]

    for b_path in backup_paths:
        assert os.path.isfile(b_path), f"Backup archive {b_path} is missing."
        assert tarfile.is_tarfile(b_path), f"File {b_path} is not a valid tar archive."

        with tarfile.open(b_path, "r:gz") as tar:
            names = tar.getnames()
            # Check if any file in the archive is named sensor.log or ends with /sensor.log
            assert any(name.endswith("sensor.log") for name in names), (
                f"Archive {b_path} does not contain 'sensor.log'."
            )

def test_backups_mtime():
    """Test that the backups were created with sleep intervals (mtimes should be distinct)."""
    b1 = "/home/user/backups/backup_1.tar.gz"
    b2 = "/home/user/backups/backup_2.tar.gz"
    b3 = "/home/user/backups/backup_3.tar.gz"

    if os.path.isfile(b1) and os.path.isfile(b2) and os.path.isfile(b3):
        mtime1 = os.path.getmtime(b1)
        mtime2 = os.path.getmtime(b2)
        mtime3 = os.path.getmtime(b3)

        assert mtime2 > mtime1, "backup_2.tar.gz is not newer than backup_1.tar.gz. Did you sleep for 1 second?"
        assert mtime3 > mtime2, "backup_3.tar.gz is not newer than backup_2.tar.gz. Did you sleep for 1 second?"