# test_final_state.py

import os
import tarfile
import pytest

def test_backup_archive_exists_and_valid():
    archive_path = "/home/user/archive/legacy_service.tar.gz"
    assert os.path.isfile(archive_path), f"Backup archive {archive_path} does not exist or is not a file."

    # Verify it is a valid gzip-compressed tar archive
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
            # Just ensure we can read it without error; optionally check if it contains expected files
            assert len(names) > 0, f"Archive {archive_path} is empty."
    except tarfile.ReadError:
        pytest.fail(f"Archive {archive_path} is not a valid gzip-compressed tar archive.")

def test_shared_logs_directory_exists():
    shared_logs_path = "/home/user/shared_logs/cloud_service"
    assert os.path.isdir(shared_logs_path), f"Shared logs directory {shared_logs_path} does not exist."

def test_logs_symlink_correct():
    symlink_path = "/home/user/cloud_service/logs"
    expected_target = "/home/user/shared_logs/cloud_service"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    actual_target = os.readlink(symlink_path)
    assert actual_target == expected_target, f"Symlink {symlink_path} points to {actual_target}, expected {expected_target}."

def test_systemd_service_file_updated():
    service_file_path = "/home/user/services/cloud-worker.service"
    assert os.path.isfile(service_file_path), f"Service file {service_file_path} does not exist."

    with open(service_file_path, "r") as f:
        content = f.read()

    assert "After=cloud-db.service" in content, "Missing 'After=cloud-db.service' in the systemd service file."
    assert "Requires=cloud-db.service" in content, "Missing 'Requires=cloud-db.service' in the systemd service file."

def test_health_check_script_exists():
    script_path = "/home/user/cloud_service/health_check.py"
    assert os.path.isfile(script_path), f"Health check script {script_path} does not exist."

def test_status_log_contains_migration_ready():
    # The symlink points to shared_logs, so checking either path is fine.
    # We'll check the resolved path.
    status_log_path = "/home/user/shared_logs/cloud_service/status.log"
    assert os.path.isfile(status_log_path), f"Status log {status_log_path} does not exist. Did the script run successfully?"

    with open(status_log_path, "r") as f:
        content = f.read().strip()

    assert content == "MIGRATION_READY", f"Expected 'MIGRATION_READY' in {status_log_path}, got '{content}'."