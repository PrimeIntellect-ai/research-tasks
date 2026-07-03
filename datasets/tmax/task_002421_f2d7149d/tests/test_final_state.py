# test_final_state.py

import os
import pytest

def test_success_file():
    path = "/home/user/success.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you complete the verification step?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert "DONE" in content, f"File {path} does not contain 'DONE'."

def test_ssh_cmd_log():
    path = "/home/user/logs/ssh_cmd.log"
    assert os.path.isfile(path), f"File {path} is missing. Did the ssh_manager.sh script run successfully?"
    with open(path, "r") as f:
        content = f.read()
    expected_cmd = "ssh -f -N -L 8080:localhost:80 mockuser@remotehost"
    assert expected_cmd in content, f"File {path} does not contain the exact expected SSH command."

def test_alert_eml():
    path = "/home/user/mail/alert.eml"
    assert os.path.isfile(path), f"File {path} is missing. Did alert.rb run and create the email?"
    with open(path, "r") as f:
        content = f.read()

    expected_content = (
        "To: admin@example.com\n"
        "Subject: Tunnel Restored\n"
        "\n"
        "Tunnel is active.\n"
    )
    assert content.strip() == expected_content.strip(), f"File {path} does not have the exact expected content."

def test_monitor_py_updates():
    path = "/home/user/supervisor/monitor.py"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    assert "/home/user/supervisor/ssh_manager.sh" in content, "monitor.py does not use the absolute path to ssh_manager.sh"
    assert "/home/user/logs/monitor_error.log" in content, "monitor.py does not use the absolute path for the error log"
    assert "/home/user/supervisor/alert.rb" in content, "monitor.py does not execute alert.rb on success"

def test_alert_rb_exists_and_executable():
    path = "/home/user/supervisor/alert.rb"
    assert os.path.isfile(path), f"Script {path} is missing."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."