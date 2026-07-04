# test_final_state.py

import os
import subprocess
import tarfile
import pytest

def test_nginx_conf_content():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    # Check for required directives
    assert "pid /home/user/nginx.pid;" in content or "pid" in content and "/home/user/nginx.pid" in content, "Missing or incorrect pid directive."
    assert "error_log /home/user/error.log;" in content or "error_log" in content and "/home/user/error.log" in content, "Missing or incorrect error_log directive."
    assert "access_log" in content and "/home/user/access.log" in content, "Missing or incorrect access_log directive."
    assert "events" in content, "Missing events block."
    assert "http" in content, "Missing http block."
    assert "listen 8080;" in content or "listen" in content and "8080" in content, "Missing or incorrect listen directive."
    assert "proxy_pass http://backend;" in content or "proxy_pass" in content and "http://backend" in content, "Missing or incorrect proxy_pass directive."
    assert "upstream backend" in content, "Missing upstream backend block."
    assert "127.0.0.1:8081" in content, "Missing backend server 127.0.0.1:8081."
    assert "127.0.0.1:8082" in content, "Missing backend server 127.0.0.1:8082."

def test_storage_and_backups_dirs():
    storage_dir = "/home/user/storage"
    backups_dir = "/home/user/backups"
    dummy_file = os.path.join(storage_dir, "dummy.txt")

    assert os.path.isdir(storage_dir), f"{storage_dir} does not exist."
    assert os.path.isdir(backups_dir), f"{backups_dir} does not exist."
    assert os.path.isfile(dummy_file), f"{dummy_file} does not exist."

    size_mb = os.path.getsize(dummy_file) / (1024 * 1024)
    assert 9 <= size_mb <= 11, f"{dummy_file} is not approximately 10MB (found {size_mb:.2f} MB)."

def test_backup_archive():
    archive_path = "/home/user/backups/storage_backup.tar.gz"
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."

    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        # Ensure that the storage directory or its contents are in the archive
        assert any("dummy.txt" in name for name in names), "dummy.txt not found in the backup archive."

def test_setup_proxy_idempotency():
    script_path = "/home/user/setup_proxy.py"
    conf_path = "/home/user/nginx.conf"

    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Run without changes
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert "CONFIG_UNCHANGED" in result.stdout, "Script did not output CONFIG_UNCHANGED when no changes were needed."

    # Modify the config file
    with open(conf_path, "a") as f:
        f.write("\n# test modification\n")

    # Run again, should update
    result2 = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert "CONFIG_UPDATED" in result2.stdout, "Script did not output CONFIG_UPDATED after the config was modified."

def test_backup_logic():
    script_path = "/home/user/backup.py"
    log_path = "/home/user/backup.log"
    storage_dir = "/home/user/storage"

    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    # Initial state check
    with open(log_path, "r") as f:
        log_content = f.read().strip()
    assert log_content == "BACKUP_SUCCESS", f"Expected BACKUP_SUCCESS in {log_path}, got {log_content}"

    # Create a 60MB file to exceed quota
    large_file = os.path.join(storage_dir, "large_test.txt")
    try:
        with open(large_file, "wb") as f:
            f.write(b"0" * (60 * 1024 * 1024))

        # Run backup script
        subprocess.run(["python3", script_path], check=True)

        # Check log again
        with open(log_path, "r") as f:
            log_content2 = f.read().strip()
        assert log_content2 == "QUOTA_EXCEEDED", f"Expected QUOTA_EXCEEDED in {log_path}, got {log_content2}"
    finally:
        # Cleanup
        if os.path.exists(large_file):
            os.remove(large_file)