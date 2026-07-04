# test_final_state.py

import os
import zipfile
import json
import pytest

def test_archive_created_and_contents():
    archive_path = "/home/user/secure_backup.zip"
    assert os.path.exists(archive_path), f"Archive file {archive_path} was not created."

    with zipfile.ZipFile(archive_path, 'r') as zf:
        namelist = zf.namelist()

        # Check presence of old files
        assert "log1.txt" in namelist, "log1.txt is missing from the archive."
        assert "subdir/log2.txt" in namelist, "subdir/log2.txt is missing from the archive."

        # Check absence of new file
        assert "log3_new.txt" not in namelist, "log3_new.txt should not be in the archive because it is not old enough."

        # Check redaction in log1.txt
        content1 = zf.read("log1.txt").decode('utf-8')
        assert "[REDACTED_EMAIL]" in content1, "Email was not redacted with [REDACTED_EMAIL] in log1.txt."
        assert "admin@example.com" not in content1, "Original email admin@example.com is still present in archived log1.txt."
        assert "user123@test.co.uk" not in content1, "Original email user123@test.co.uk is still present in archived log1.txt."

        # Check redaction in subdir/log2.txt
        content2 = zf.read("subdir/log2.txt").decode('utf-8')
        assert "[REDACTED_EMAIL]" in content2, "Email was not redacted with [REDACTED_EMAIL] in subdir/log2.txt."
        assert "support@domain.com" not in content2, "Original email support@domain.com is still present in archived subdir/log2.txt."

def test_original_files_deleted():
    log1_path = "/home/user/app_logs/log1.txt"
    log2_path = "/home/user/app_logs/subdir/log2.txt"

    assert not os.path.exists(log1_path), f"Old log file {log1_path} was not deleted from disk."
    assert not os.path.exists(log2_path), f"Old log file {log2_path} was not deleted from disk."

def test_recent_file_untouched():
    log3_path = "/home/user/app_logs/log3_new.txt"

    assert os.path.exists(log3_path), f"Recent log file {log3_path} was incorrectly deleted."

    with open(log3_path, "r") as f:
        content3 = f.read()

    assert "hello@world.com" in content3, f"Recent log file {log3_path} was incorrectly redacted or modified."
    assert "[REDACTED_EMAIL]" not in content3, f"Recent log file {log3_path} was incorrectly redacted."