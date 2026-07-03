import os
import subprocess
import pytest

def test_verify_backup_script_exists():
    assert os.path.isfile("/home/user/verify_backup.py"), "verify_backup.py is missing from /home/user/"

def test_verify_backup_clean_corpus():
    script_path = "/home/user/verify_backup.py"
    clean_dir = "/app/corpora/clean/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(('.tar', '.tar.gz'))]
    assert len(clean_files) > 0, "No clean corpus files found to test"

    failed_files = []
    for f in clean_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {failed_files}"

def test_verify_backup_evil_corpus():
    script_path = "/home/user/verify_backup.py"
    evil_dir = "/app/corpora/evil/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(('.tar', '.tar.gz'))]
    assert len(evil_files) > 0, "No evil corpus files found to test"

    failed_files = []
    for f in evil_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {failed_files}"

def test_restore_report_content():
    report_path = "/home/user/restore_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing"

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_token = "SYSTEM_RESTORE_SUCCESS_TOKEN_99812"
    assert expected_token in content, f"Report file does not contain the expected token. Found: {content}"