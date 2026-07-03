# test_final_state.py
import os
import hashlib
import pytest

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    assert len(lines) == 4, f"Expected exactly 4 lines in {report_path}, found {len(lines)}."

    assert lines[0] == "backup_worker.py", f"Line 1 (script name) is incorrect. Got: {lines[0]}"
    assert lines[1] == "x9F2kL1pQ8zT4wR!", f"Line 2 (leaked key) is incorrect. Got: {lines[1]}"
    assert lines[2] == "DEVSECOPS_FLAG_998822", f"Line 3 (decrypted text) is incorrect. Got: {lines[2]}"

    expected_hash = hashlib.sha256(b"DEVSECOPS_FLAG_998822").hexdigest()
    assert lines[3] == expected_hash, f"Line 4 (SHA256 hash) is incorrect. Got: {lines[3]}"

def test_backup_worker_refactored():
    script_path = "/home/user/app/backup_worker.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "--key" not in content, "The script still contains the '--key' argument which violates the policy."
    assert "BACKUP_KEY" in content, "The script does not appear to read the 'BACKUP_KEY' environment variable."