# test_final_state.py

import os

def test_config_file_updated():
    config_path = "/home/user/backup_config.txt"
    assert os.path.isfile(config_path), f"File {config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read()
    assert "/home/user/backups" in content, "The config file does not contain the new path '/home/user/backups'."
    assert "/var/old_backups" not in content, "The config file still contains the old path '/var/old_backups'."

def test_vulnerable_archives_log():
    log_path = "/home/user/vulnerable_archives.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."
    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Check if lines are sorted alphabetically and contain the correct entries
    assert lines == sorted(lines), f"Lines in {log_path} are not sorted alphabetically."
    expected = ["backup_absolute.zip", "backup_malicious.zip"]
    assert sorted(lines) == expected, f"Expected {expected} in {log_path}, got {lines}."

def test_safe_archives_log():
    log_path = "/home/user/safe_archives.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."
    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Check if lines are sorted alphabetically and contain the correct entries
    assert lines == sorted(lines), f"Lines in {log_path} are not sorted alphabetically."
    expected = ["backup_safe1.zip", "backup_safe2.zip"]
    assert sorted(lines) == expected, f"Expected {expected} in {log_path}, got {lines}."

def test_extracted_files():
    safe1 = "/home/user/extracted/safe1.txt"
    safe2 = "/home/user/extracted/safe2.txt"
    assert os.path.isfile(safe1), f"Safe extracted file {safe1} is missing."
    assert os.path.isfile(safe2), f"Safe extracted file {safe2} is missing."

def test_malicious_files_not_extracted():
    evil1 = "/home/user/extracted/evil.sh"
    evil2 = "/home/user/evil.sh"
    evil3 = "/etc/passwd_overwrite"
    assert not os.path.exists(evil1), f"Malicious file {evil1} was extracted!"
    assert not os.path.exists(evil2), f"Malicious file {evil2} was extracted!"
    assert not os.path.exists(evil3), f"Malicious file {evil3} was extracted!"