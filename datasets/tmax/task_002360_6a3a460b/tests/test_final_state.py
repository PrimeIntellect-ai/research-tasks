# test_final_state.py

import os
import tarfile
import pytest
import tempfile

def test_summary_txt():
    """Verify the summary.txt contains the correct count."""
    summary_path = "/home/user/backups/summary.txt"
    assert os.path.isfile(summary_path), f"File missing: {summary_path}"

    with open(summary_path, 'r') as f:
        content = f.read().strip()

    assert content == "3", f"Expected summary.txt to contain '3', but got '{content}'"

def test_clean_logs_archive_exists_and_valid():
    """Verify the clean_logs.tar.gz archive exists and contains the correct files."""
    archive_path = "/home/user/backups/clean_logs.tar.gz"
    assert os.path.isfile(archive_path), f"File missing: {archive_path}"

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        assert "app1.log" in names, "app1.log missing from clean_logs.tar.gz"
        assert "app2.log" in names, "app2.log missing from clean_logs.tar.gz"

        # Extract to verify contents
        with tempfile.TemporaryDirectory() as tmpdir:
            tar.extractall(path=tmpdir)

            with open(os.path.join(tmpdir, "app1.log"), 'r') as f:
                app1_content = f.read()
            with open(os.path.join(tmpdir, "app2.log"), 'r') as f:
                app2_content = f.read()

            # Validate DEPRECATED_SRV is completely gone
            assert "DEPRECATED_SRV" not in app1_content, "DEPRECATED_SRV found in app1.log"
            assert "DEPRECATED_SRV" not in app2_content, "DEPRECATED_SRV found in app2.log"

            # Validate WEB_01 kept its original error code 401
            assert "ErrorCode: 401" in app1_content, "ErrorCode: 401 missing from app1.log"

            # Validate DB_01 got the ErrorCode: 0000 inserted
            assert "ErrorCode: 0000\n[END_RECORD]" in app2_content, "ErrorCode: 0000 not inserted correctly in app2.log"

            # Validate WEB_02 got the ErrorCode: 0000 inserted
            assert "ErrorCode: 0000\n[END_RECORD]" in app1_content, "ErrorCode: 0000 not inserted correctly in app1.log"

def test_processing_directory_logs():
    """Verify the processing directory contains the sanitized logs."""
    app1_path = "/home/user/processing/app1.log"
    app2_path = "/home/user/processing/app2.log"

    assert os.path.isfile(app1_path), f"File missing: {app1_path}"
    assert os.path.isfile(app2_path), f"File missing: {app2_path}"

    with open(app1_path, 'r') as f:
        app1_content = f.read()
    with open(app2_path, 'r') as f:
        app2_content = f.read()

    assert "DEPRECATED_SRV" not in app1_content, "DEPRECATED_SRV found in processed app1.log"
    assert "DEPRECATED_SRV" not in app2_content, "DEPRECATED_SRV found in processed app2.log"
    assert "ErrorCode: 401" in app1_content, "ErrorCode: 401 missing from processed app1.log"
    assert "ErrorCode: 0000\n[END_RECORD]" in app2_content, "ErrorCode: 0000 not inserted correctly in processed app2.log"
    assert "ErrorCode: 0000\n[END_RECORD]" in app1_content, "ErrorCode: 0000 not inserted correctly in processed app1.log"