# test_final_state.py

import os
import pytest

def test_monitor_go_exists():
    assert os.path.isfile("/home/user/monitor.go"), "The Go program /home/user/monitor.go does not exist."

def test_monitor_log_contents():
    log_path = "/home/user/monitor.log"
    assert os.path.isfile(log_path), f"The log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read()

    assert "ERROR: Broken link legacy_data" in content, "The log file does not contain the expected error for the broken link 'legacy_data'."
    assert "WARN: Email server unreachable" in content, "The log file does not contain the expected warning for the unreachable email server."

def test_mail_spool_alerts():
    spool_dir = "/home/user/mail_spool"
    assert os.path.isdir(spool_dir), f"The mail spool directory {spool_dir} does not exist."

    user_data_alert = os.path.join(spool_dir, "alert_user_data.txt")
    backup_data_alert = os.path.join(spool_dir, "alert_backup_data.txt")
    app_data_alert = os.path.join(spool_dir, "alert_app_data.txt")
    legacy_data_alert = os.path.join(spool_dir, "alert_legacy_data.txt")

    assert os.path.isfile(user_data_alert), f"Expected alert file {user_data_alert} was not created."
    assert os.path.isfile(backup_data_alert), f"Expected alert file {backup_data_alert} was not created."

    assert not os.path.exists(app_data_alert), f"Alert file {app_data_alert} should not exist (under quota)."
    assert not os.path.exists(legacy_data_alert), f"Alert file {legacy_data_alert} should not exist (broken link)."

    # Calculate expected sizes
    node2_size = sum(os.path.getsize(os.path.join("/home/user/storage_nodes/node2", f)) for f in os.listdir("/home/user/storage_nodes/node2") if os.path.isfile(os.path.join("/home/user/storage_nodes/node2", f)))
    node3_size = sum(os.path.getsize(os.path.join("/home/user/storage_nodes/node3", f)) for f in os.listdir("/home/user/storage_nodes/node3") if os.path.isfile(os.path.join("/home/user/storage_nodes/node3", f)))

    with open(user_data_alert, "r") as f:
        user_content = f.read().strip()

    expected_user_content = f"To: admin@local\nSubject: Quota exceeded for user_data\nSize: {node2_size}"
    assert user_content == expected_user_content, f"Content of {user_data_alert} is incorrect. Expected:\n{expected_user_content}\nGot:\n{user_content}"

    with open(backup_data_alert, "r") as f:
        backup_content = f.read().strip()

    expected_backup_content = f"To: admin@local\nSubject: Quota exceeded for backup_data\nSize: {node3_size}"
    assert backup_content == expected_backup_content, f"Content of {backup_data_alert} is incorrect. Expected:\n{expected_backup_content}\nGot:\n{backup_content}"

def test_no_extra_alert_files():
    spool_dir = "/home/user/mail_spool"
    files = [f for f in os.listdir(spool_dir) if os.path.isfile(os.path.join(spool_dir, f))]
    expected_files = {"alert_user_data.txt", "alert_backup_data.txt"}
    actual_files = set(files)
    assert actual_files == expected_files, f"Found unexpected files in {spool_dir}: {actual_files - expected_files}"