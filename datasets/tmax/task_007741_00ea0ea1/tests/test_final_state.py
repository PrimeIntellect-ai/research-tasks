# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_setup_script_exists_and_executable():
    """Verify that the setup script exists and is executable."""
    path = "/home/user/setup_migration.sh"
    assert os.path.isfile(path), f"Setup script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Setup script {path} is not executable."

def test_haproxy_cfg_contents():
    """Verify that the haproxy.cfg contains the required configurations."""
    path = "/home/user/haproxy.cfg"
    assert os.path.isfile(path), f"HAProxy config {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "timeout connect 5000ms" in content, "Missing 'timeout connect 5000ms' in haproxy.cfg"
    assert "timeout client 10000ms" in content, "Missing 'timeout client 10000ms' in haproxy.cfg"
    assert "timeout server 10000ms" in content, "Missing 'timeout server 10000ms' in haproxy.cfg"

    assert "frontend email_front" in content, "Missing 'frontend email_front' in haproxy.cfg"
    assert "bind 127.0.0.1:8080" in content, "Missing 'bind 127.0.0.1:8080' in haproxy.cfg"

    assert "backend email_back" in content, "Missing 'backend email_back' in haproxy.cfg"
    assert "127.0.0.1:8081" in content, "Missing node1 at '127.0.0.1:8081' in haproxy.cfg"
    assert "127.0.0.1:8082" in content, "Missing node2 at '127.0.0.1:8082' in haproxy.cfg"
    assert "roundrobin" in content, "Missing 'roundrobin' load balancing in haproxy.cfg"

def test_storage_monitor_script_exists_and_executable():
    """Verify that the storage_monitor.sh exists and is executable."""
    path = "/home/user/storage_monitor.sh"
    assert os.path.isfile(path), f"Monitor script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Monitor script {path} is not executable."

def test_storage_monitor_under_limits(tmp_path):
    """Test storage_monitor.sh behavior when under 1024 KB."""
    monitor_script = "/home/user/storage_monitor.sh"
    mail_spool = "/home/user/mail_spool"
    migration_log = "/home/user/migration.log"

    # Clear log and spool
    open(migration_log, "w").close()
    for f in os.listdir(mail_spool):
        os.remove(os.path.join(mail_spool, f))

    # Create a 500KB file
    small_file = os.path.join(mail_spool, "small.txt")
    with open(small_file, "wb") as f:
        f.write(b"0" * 500 * 1024)

    # Run monitor script
    subprocess.run([monitor_script], check=True)

    # Check log
    with open(migration_log, "r") as f:
        log_content = f.read()
    assert "[OK] Storage within limits." in log_content, "Expected '[OK] Storage within limits.' in migration.log"

    # Check file still exists
    assert os.path.isfile(small_file), "small.txt should not have been deleted."

def test_storage_monitor_exceeding_limits():
    """Test storage_monitor.sh behavior when over 1024 KB."""
    monitor_script = "/home/user/storage_monitor.sh"
    mail_spool = "/home/user/mail_spool"
    migration_log = "/home/user/migration.log"

    # Clear log and spool
    open(migration_log, "w").close()
    for f in os.listdir(mail_spool):
        os.remove(os.path.join(mail_spool, f))

    # Create a 2000KB file
    large_file = os.path.join(mail_spool, "large.txt")
    with open(large_file, "wb") as f:
        f.write(b"0" * 2000 * 1024)

    # Run monitor script
    subprocess.run([monitor_script], check=True)

    # Check log
    with open(migration_log, "r") as f:
        log_content = f.read()
    assert "[WARN] Storage quota exceeded. Clearing spool." in log_content, "Expected '[WARN] Storage quota exceeded. Clearing spool.' in migration.log"

    # Check spool is empty
    files = os.listdir(mail_spool)
    assert len(files) == 0, f"mail_spool should be empty, but found: {files}"