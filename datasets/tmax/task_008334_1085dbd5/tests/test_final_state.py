# test_final_state.py
import os
import pytest

def test_rejected_updates_log():
    log_path = "/home/user/rejected_updates.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = set(line.strip() for line in f if line.strip())

    expected_lines = {
        "../../../home/user/.bash_profile",
        "plugins/../../shadow_backup.conf"
    }

    assert lines == expected_lines, f"Expected {expected_lines} in rejected_updates.log, but got {lines}."

def test_config_ledger():
    ledger_path = "/home/user/config_ledger.txt"
    assert os.path.isfile(ledger_path), f"File {ledger_path} does not exist."

    with open(ledger_path, 'r') as f:
        lines = set(line.strip() for line in f if line.strip())

    expected_lines = {
        "[UPDATE] network.conf | port=8080",
        "[UPDATE] network.conf | host=0.0.0.0",
        "[UPDATE] plugins/db.conf | engine=sqlite",
        "[UPDATE] plugins/db.conf | workers=4"
    }

    assert lines == expected_lines, f"Expected {expected_lines} in config_ledger.txt, but got {lines}."

def test_extracted_files_exist():
    file1 = "/home/user/app_configs/network.conf"
    file2 = "/home/user/app_configs/plugins/db.conf"

    assert os.path.isfile(file1), f"Valid extracted file {file1} is missing."
    assert os.path.isfile(file2), f"Valid extracted file {file2} is missing."

def test_malicious_files_not_extracted():
    # Check that the malicious files were not extracted
    file1 = "/home/user/.bash_profile"
    file2 = "/home/user/shadow_backup.conf"

    if os.path.exists(file1):
        with open(file1, 'r') as f:
            content = f.read()
            assert 'echo "hacked"' not in content, f"Malicious content found in {file1}."

    assert not os.path.exists(file2), f"Malicious file {file2} was extracted!"