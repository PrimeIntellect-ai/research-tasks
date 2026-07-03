# test_final_state.py

import os
import subprocess
import tarfile
import pytest

def test_drop_count():
    count_file = "/home/user/drop_count.txt"
    assert os.path.exists(count_file), f"File {count_file} does not exist."
    with open(count_file, "r") as f:
        content = f.read().strip()
    assert content == "14", f"Expected drop count to be '14', but got '{content}'."

def test_log_classifier_adversarial():
    script_path = "/home/user/log_classifier.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run([script_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    assert not error_messages, "Adversarial corpus test failed: " + "; ".join(error_messages)

def test_backup_tarball():
    backup_path = "/home/user/backup.tar.gz"
    assert os.path.exists(backup_path), f"Backup tarball {backup_path} does not exist."
    assert tarfile.is_tarfile(backup_path), f"File {backup_path} is not a valid tar archive."

    with tarfile.open(backup_path, "r:gz") as tar:
        names = tar.getnames()
        # Check if netmon_config is in the tarball (could be just the directory or its contents)
        assert any("netmon_config" in name for name in names), "Tarball does not contain 'netmon_config'."

def test_systemd_service():
    service_path = "/home/user/.config/systemd/user/log-filter.service"
    assert os.path.exists(service_path), f"Systemd service file {service_path} does not exist."

    with open(service_path, "r") as f:
        content = f.read()

    assert "[Unit]" in content, f"{service_path} is missing [Unit] section."
    assert "[Service]" in content, f"{service_path} is missing [Service] section."
    assert "ExecStart=/home/user/log_classifier.sh" in content, f"{service_path} is missing correct ExecStart directive."

def test_bashrc_env_var():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"{bashrc_path} does not exist."

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert "export FILTER_STRICT=1" in content, f"'export FILTER_STRICT=1' not found in {bashrc_path}."