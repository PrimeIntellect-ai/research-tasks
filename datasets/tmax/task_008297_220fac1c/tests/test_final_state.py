# test_final_state.py

import os
import json
import pytest

DATA_DIR = "/home/user/data"
ARCHIVE_DIR = "/home/user/archive"
DEPLOY_RC = "/home/user/.deploy_rc"
SCRIPT_PATH = "/home/user/storage_janitor.py"
REPORT_PATH = "/home/user/janitor_report.json"

def test_deploy_rc_exists_and_exports():
    assert os.path.exists(DEPLOY_RC), f"{DEPLOY_RC} does not exist"
    with open(DEPLOY_RC, "r") as f:
        content = f.read()

    assert "JANITOR_DATA_DIR=/home/user/data" in content, "Missing or incorrect JANITOR_DATA_DIR export in .deploy_rc"
    assert "JANITOR_ARCHIVE_DIR=/home/user/archive" in content, "Missing or incorrect JANITOR_ARCHIVE_DIR export in .deploy_rc"
    assert "JANITOR_QUOTA_KB=1500" in content, "Missing or incorrect JANITOR_QUOTA_KB export in .deploy_rc"

def test_archive_dir_exists():
    assert os.path.isdir(ARCHIVE_DIR), f"{ARCHIVE_DIR} is not a directory or does not exist"

def test_files_moved_correctly():
    # Processed files should be in archive
    for f in ["file1.txt", "file3.txt"]:
        archive_path = os.path.join(ARCHIVE_DIR, f)
        assert os.path.exists(archive_path), f"{f} was not moved to the archive directory"
        data_path = os.path.join(DATA_DIR, f)
        assert not os.path.exists(data_path), f"{f} should no longer exist in the data directory"

    # Unprocessed files should remain in data
    for f in ["file2.txt", "file4.txt"]:
        data_path = os.path.join(DATA_DIR, f)
        assert os.path.exists(data_path), f"{f} should remain in the data directory"
        archive_path = os.path.join(ARCHIVE_DIR, f)
        assert not os.path.exists(archive_path), f"{f} should not have been moved to the archive directory"

def test_script_exists_and_uses_subprocess():
    assert os.path.exists(SCRIPT_PATH), f"{SCRIPT_PATH} does not exist"
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    assert "subprocess" in content, "The script does not seem to use the subprocess module"
    assert "grep" in content, "The script does not seem to use grep"
    assert "awk" in content, "The script does not seem to use awk"

def test_janitor_report_json():
    assert os.path.exists(REPORT_PATH), f"{REPORT_PATH} does not exist"

    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not valid JSON")

    assert "initial_size_kb" in report, "Missing 'initial_size_kb' in report"
    assert "quota_exceeded" in report, "Missing 'quota_exceeded' in report"
    assert "files_archived" in report, "Missing 'files_archived' in report"
    assert "final_size_kb" in report, "Missing 'final_size_kb' in report"

    assert report["quota_exceeded"] is True, "'quota_exceeded' should be true"

    archived = report["files_archived"]
    assert isinstance(archived, list), "'files_archived' must be a list"
    assert set(archived) == {"file1.txt", "file3.txt"}, f"Expected file1.txt and file3.txt to be archived, got {archived}"

    assert isinstance(report["initial_size_kb"], (int, float)), "'initial_size_kb' must be a number"
    assert report["initial_size_kb"] > 2000, "Initial size should be > 2000 KB"

    assert isinstance(report["final_size_kb"], (int, float)), "'final_size_kb' must be a number"
    assert report["final_size_kb"] < 1500, "Final size should be < 1500 KB"