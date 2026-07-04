# test_final_state.py

import os
import json
import pytest

def test_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_directories_created():
    """Test that the required directories were created."""
    assert os.path.isdir("/home/user/archive"), "Directory /home/user/archive was not created."
    assert os.path.isdir("/home/user/reports"), "Directory /home/user/reports was not created."

def test_archives_exist():
    """Test that the correct files were archived and compressed."""
    assert os.path.isfile("/home/user/archive/db_backup.log.gz"), "Archive /home/user/archive/db_backup.log.gz is missing."
    assert os.path.isfile("/home/user/archive/syslog.log.gz"), "Archive /home/user/archive/syslog.log.gz is missing."

def test_original_archived_files_removed():
    """Test that the original files that were archived are no longer in the logs_pool."""
    assert not os.path.exists("/home/user/logs_pool/db_backup.log"), "Original file db_backup.log should have been moved/removed."
    assert not os.path.exists("/home/user/logs_pool/syslog.log"), "Original file syslog.log should have been moved/removed."

def test_retain_file_untouched():
    """Test that the file marked as 'retain' was left in the logs_pool."""
    assert os.path.isfile("/home/user/logs_pool/web_access.log"), "File web_access.log should have been retained in /home/user/logs_pool."
    assert not os.path.exists("/home/user/archive/web_access.log.gz"), "File web_access.log should not have been archived."

def test_summary_report():
    """Test that the summary JSON report contains the correct calculations."""
    report_path = "/home/user/reports/summary.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert "archived_count" in data, "Key 'archived_count' missing in summary.json."
    assert "freed_bytes" in data, "Key 'freed_bytes' missing in summary.json."

    assert data["archived_count"] == 2, f"Expected archived_count to be 2, got {data['archived_count']}."

    # db_backup.log (2097152) + syslog.log (524288) = 2621440
    expected_bytes = 2097152 + 524288
    assert data["freed_bytes"] == expected_bytes, f"Expected freed_bytes to be {expected_bytes}, got {data['freed_bytes']}."