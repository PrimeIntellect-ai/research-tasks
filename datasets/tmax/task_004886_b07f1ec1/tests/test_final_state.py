# test_final_state.py

import os
import tarfile
import socket
import re
import shutil
import pytest

APP_ENV_DIR = "/home/user/app_env"

def test_backup_exists_and_valid():
    backup_path = os.path.join(APP_ENV_DIR, "backups", "config_backup.tar.gz")
    assert os.path.isfile(backup_path), f"Backup file {backup_path} is missing."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # Check if settings.conf and network.conf are in the tarball
            # They might be prefixed with config/ or absolute paths
            found_settings = any(name.endswith("settings.conf") for name in names)
            found_network = any(name.endswith("network.conf") for name in names)
            assert found_settings, "settings.conf not found in the backup tarball."
            assert found_network, "network.conf not found in the backup tarball."
    except tarfile.TarError:
        pytest.fail(f"Backup file {backup_path} is not a valid gzip-compressed tarball.")

def test_symlink_fixed():
    symlink_path = os.path.join(APP_ENV_DIR, "sockets", "upstream.sock")
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    target = os.readlink(symlink_path)
    expected_target = "/home/user/app_env/run/backend.sock"
    assert target == expected_target, f"Symlink {symlink_path} points to {target} instead of {expected_target}."

def test_backend_compiled():
    bin_path = os.path.join(APP_ENV_DIR, "bin", "backend")
    assert os.path.isfile(bin_path), f"Compiled executable {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_verify_log_content():
    log_path = os.path.join(APP_ENV_DIR, "verify.log")
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    match = re.match(r"^OK:\s*(\d+)$", content)
    assert match, f"Log file {log_path} does not match the expected format 'OK: <bytes>'. Content: {content}"

    # We can also check if the bytes are somewhat reasonable (e.g., > 0)
    bytes_avail = int(match.group(1))
    assert bytes_avail > 0, "Available bytes reported in log should be greater than 0."

def test_backend_daemon_running_and_responds():
    sock_path = os.path.join(APP_ENV_DIR, "sockets", "upstream.sock")
    assert os.path.exists(sock_path), f"Socket file {sock_path} does not exist. Is the daemon running?"

    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(sock_path)
        client.sendall(b"STATUS\n")
        response = client.recv(1024).decode("utf-8")
    except Exception as e:
        pytest.fail(f"Failed to communicate with the daemon via {sock_path}: {e}")
    finally:
        client.close()

    match = re.match(r"^OK:\s*(\d+)\n?$", response)
    assert match, f"Daemon response did not match 'OK: <bytes>\\n'. Response: {response}"

    # Verify the reported space matches std::filesystem::space("/home/user").available
    # Python's shutil.disk_usage gives similar results, though there might be slight discrepancies
    # depending on timing, so we check if it's a valid integer and roughly matches.
    reported_bytes = int(match.group(1))
    statvfs = os.statvfs("/home/user")
    actual_avail = statvfs.f_bavail * statvfs.f_frsize

    # Allow a margin of error (e.g. 50MB) due to concurrent disk activity
    margin = 50 * 1024 * 1024
    assert abs(reported_bytes - actual_avail) < margin, f"Reported bytes {reported_bytes} differs significantly from actual available bytes {actual_avail}."