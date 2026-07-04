# test_final_state.py

import os
import subprocess
import socket
import pytest

def test_tunnel_active():
    """Verify that the SSH tunnel is listening on the LOCAL_TUNNEL_PORT (5050)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('localhost', 5050))
        assert result == 0, "SSH tunnel is not listening on port 5050. Ensure the tunnel forwards 5050 to 8443."

def test_cron_job_installed():
    """Verify that a cron job is installed for the user account."""
    try:
        # Run crontab -l for the current user (which should be 'user' or root checking 'user')
        result = subprocess.run(["crontab", "-l", "-u", "user"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # If running as user, just crontab -l might be needed, but -u user works if root.
        if result.returncode != 0:
            result = subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        assert result.returncode == 0, "No crontab found for the user."
        assert len(result.stdout.strip()) > 0, "Crontab is empty. The agent must be scheduled."
    except Exception as e:
        pytest.fail(f"Failed to check cron jobs: {e}")

def test_rust_project_built():
    """Verify that the Rust project was built in release mode."""
    release_dir = "/home/user/backup_agent/target/release"
    assert os.path.isdir(release_dir), f"Rust release directory not found at {release_dir}. Did you build in release mode?"

    # Check if there's an executable file in the release directory (excluding directories and .d files)
    executables = []
    for root, dirs, files in os.walk(release_dir):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath) and os.access(filepath, os.X_OK) and not file.endswith('.d'):
                executables.append(filepath)

    assert len(executables) > 0, "No executable found in the Rust release directory."

def test_backup_received_and_size():
    """
    Verify that the backup payload was received and meets the compression threshold.
    Metric: File size of /home/user/received_backup.dat
    Threshold: <= 50000 bytes
    """
    target_file = "/home/user/received_backup.dat"
    assert os.path.isfile(target_file), f"The backup payload was not found at {target_file}. The mock listener didn't receive the data."

    file_size = os.path.getsize(target_file)
    threshold = 50000

    assert file_size > 0, f"The received backup file at {target_file} is empty."
    assert file_size <= threshold, (
        f"Compression insufficient or payload too large. "
        f"Measured size: {file_size} bytes. Threshold: {threshold} bytes."
    )