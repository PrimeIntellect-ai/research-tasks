# test_final_state.py

import os
import subprocess
import pytest

def test_directories_and_symlink():
    """Test that the required directories and symlink are created correctly."""
    assert os.path.isdir("/home/user/storage/net_logs"), "Directory /home/user/storage/net_logs does not exist."
    assert os.path.isdir("/home/user/mail"), "Directory /home/user/mail does not exist."

    assert os.path.islink("/home/user/logs"), "/home/user/logs is not a symlink."
    target = os.readlink("/home/user/logs")
    assert target == "/home/user/storage/net_logs", f"Symlink /home/user/logs points to {target} instead of /home/user/storage/net_logs."

def test_my_fstab():
    """Test that my_fstab contains the correct mount entry."""
    fstab_path = "/home/user/my_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read()

    expected_line = "//10.0.0.50/netdata /home/user/storage/net_logs cifs defaults,ro 0 0"
    assert expected_line in content, f"The expected line was not found in {fstab_path}."

def test_script_executable():
    """Test that the net_alert.sh script exists and is executable."""
    script_path = "/home/user/net_alert.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_behavior():
    """Test the behavior of the net_alert.sh script by running it on a mock log file."""
    script_path = "/home/user/net_alert.sh"
    log_path = "/home/user/logs/sensor.log"
    alerts_path = "/home/user/mail/alerts.txt"

    # Remove alerts.txt if it exists to ensure a clean test
    if os.path.exists(alerts_path):
        os.remove(alerts_path)

    # Create mock log file
    mock_log_content = """2023-10-12T10:00:00Z IP=192.168.1.10 STATE=UP PING=12
2023-10-12T10:01:00Z IP=192.168.1.15 STATE=DOWN PING=-1
2023-10-12T10:02:00Z IP=10.0.0.2 STATE=UP PING=5
2023-10-12T10:03:00Z IP=192.168.1.99 STATE=DOWN PING=-1
"""
    with open(log_path, "w") as f:
        f.write(mock_log_content)

    # Run the script
    result = subprocess.run([script_path, log_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script exited with non-zero return code: {result.returncode}\nStderr: {result.stderr}"

    # Check alerts.txt
    assert os.path.isfile(alerts_path), f"Alerts file {alerts_path} was not created."
    with open(alerts_path, "r") as f:
        alerts_content = f.read().strip()

    expected_alerts = "ALERT: Host 192.168.1.15 is DOWN\nALERT: Host 192.168.1.99 is DOWN"
    assert alerts_content == expected_alerts, f"Alerts content is incorrect.\nExpected:\n{expected_alerts}\nGot:\n{alerts_content}"

    # Check rotation
    bak_path = f"{log_path}.bak"
    assert os.path.isfile(bak_path), f"Backup file {bak_path} was not created."
    with open(bak_path, "r") as f:
        bak_content = f.read()
    assert bak_content == mock_log_content, "Backup file does not contain the original log data."

    assert os.path.isfile(log_path), "New empty log file was not created."
    assert os.path.getsize(log_path) == 0, f"New log file {log_path} is not empty."