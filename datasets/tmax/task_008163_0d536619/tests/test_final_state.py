# test_final_state.py

import os
import re
import socket
import subprocess
import time
import tarfile
import pytest

def test_rust_cost_analyzer():
    """Verify the Rust cost-analyzer project exists, builds, and calculates correctly."""
    project_dir = "/home/user/cost-analyzer"
    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."

    # Build the binary
    build_result = subprocess.run(["cargo", "build", "--release"], cwd=project_dir, capture_output=True)
    assert build_result.returncode == 0, f"Failed to build Rust project: {build_result.stderr.decode()}"

    binary_path = os.path.join(project_dir, "target", "release", "cost-analyzer")
    if not os.path.exists(binary_path):
        # Fallback to debug if release wasn't built correctly, though prompt asked for release check
        binary_path = os.path.join(project_dir, "target", "debug", "cost-analyzer")

    assert os.path.exists(binary_path), "Compiled binary 'cost-analyzer' not found."

    # Run the binary on a test port
    test_port = 9999
    process = subprocess.Popen([binary_path, str(test_port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for the server to start
        time.sleep(1)

        # Test connection and calculation
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("127.0.0.1", test_port))
        s.sendall(b"200\n")
        response = s.recv(1024).decode("utf-8")
        s.close()

        assert response.strip() == "30.00", f"Expected '30.00', got '{response.strip()}'"
    finally:
        process.terminate()
        process.wait()

def test_haproxy_cfg():
    """Verify the HAProxy configuration file."""
    cfg_path = "/home/user/haproxy.cfg"
    assert os.path.isfile(cfg_path), f"HAProxy config {cfg_path} does not exist."

    with open(cfg_path, "r") as f:
        content = f.read()

    assert "127.0.0.1:8080" in content, "HAProxy config missing listen on 127.0.0.1:8080"
    assert "127.0.0.1:8081" in content, "HAProxy config missing backend 127.0.0.1:8081"
    assert "127.0.0.1:8082" in content, "HAProxy config missing backend 127.0.0.1:8082"
    assert "127.0.0.1:8083" in content, "HAProxy config missing backend 127.0.0.1:8083"

    # Validate config syntax
    result = subprocess.run(["haproxy", "-c", "-f", cfg_path], capture_output=True)
    assert result.returncode == 0, f"HAProxy config is invalid: {result.stderr.decode()}"

def test_supervisor_script():
    """Verify the supervisor.sh script."""
    script_path = "/home/user/supervisor.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    # Check for some looping construct
    assert re.search(r'\b(while|for|until)\b', content), "supervisor.sh does not contain a loop for monitoring."
    assert "8081" in content and "8082" in content and "8083" in content, "supervisor.sh does not reference the expected ports."

def test_fstab_entry():
    """Verify the fstab_entry.txt file."""
    fstab_path = "/home/user/fstab_entry.txt"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    pattern = r"tmpfs\s+/home/user/reports\s+tmpfs\s+.*size=50M.*uid=1000.*gid=1000.*\s+0\s+0"
    assert re.search(pattern, content), f"fstab entry does not match expected format. Got: {content}"

def test_backup_script():
    """Verify the backup.sh script."""
    script_path = "/home/user/backup.sh"
    reports_dir = "/home/user/reports"
    backups_dir = "/home/user/backups"
    archive_path = os.path.join(backups_dir, "reports_backup.tar.gz")

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Setup dummy environment
    os.makedirs(reports_dir, exist_ok=True)
    dummy_file = os.path.join(reports_dir, "test.txt")
    with open(dummy_file, "w") as f:
        f.write("dummy content")

    # Run backup script
    result = subprocess.run([script_path], capture_output=True)
    assert result.returncode == 0, f"Backup script failed: {result.stderr.decode()}"

    assert os.path.isfile(archive_path), f"Backup archive {archive_path} was not created."

    # Verify contents
    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        # The tar structure might vary depending on how they archived it (absolute vs relative)
        assert any(name.endswith("test.txt") for name in names), "test.txt not found in backup archive."