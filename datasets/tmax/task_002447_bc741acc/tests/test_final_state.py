# test_final_state.py

import os
import tarfile
import pytest

def test_directories_exist():
    """Verify that incoming and outgoing directories exist."""
    assert os.path.isdir("/home/user/incoming"), "/home/user/incoming directory does not exist."
    assert os.path.isdir("/home/user/outgoing"), "/home/user/outgoing directory does not exist."

def test_script_exists_and_executable():
    """Verify the organizer script exists and is executable."""
    script_path = "/home/user/organizer.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_incoming_empty():
    """Verify that incoming directory is empty of .tar.gz files."""
    incoming_files = os.listdir("/home/user/incoming")
    tar_gz_files = [f for f in incoming_files if f.endswith(".tar.gz")]
    assert len(tar_gz_files) == 0, f"/home/user/incoming still contains .tar.gz files: {tar_gz_files}"

def test_log_file_contents():
    """Verify that the log file contains the correct entries."""
    log_path = "/home/user/organizer.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "PROCESSED: legacy_code_A.tar.gz | CONVERTED_FILES: 2",
        "PROCESSED: legacy_code_B.tar.gz | CONVERTED_FILES: 1"
    }

    actual_lines_set = set(lines)
    for expected in expected_lines:
        assert expected in actual_lines_set, f"Expected log entry '{expected}' not found in {log_path}."

def test_outgoing_archives():
    """Verify the outgoing archives exist and contain the correctly converted UTF-8 files."""
    outgoing_dir = "/home/user/outgoing"
    archive_a = os.path.join(outgoing_dir, "legacy_code_A.tar.gz")
    archive_b = os.path.join(outgoing_dir, "legacy_code_B.tar.gz")

    assert os.path.isfile(archive_a), f"Archive {archive_a} is missing."
    assert os.path.isfile(archive_b), f"Archive {archive_b} is missing."

    # Check legacy_code_A.tar.gz
    with tarfile.open(archive_a, "r:gz") as tar:
        members = tar.getnames()
        assert "projectA/main.src" in members, "projectA/main.src missing in legacy_code_A.tar.gz"
        assert "projectA/utils/helper.src" in members, "projectA/utils/helper.src missing in legacy_code_A.tar.gz"
        assert "projectA/readme.txt" in members, "projectA/readme.txt missing in legacy_code_A.tar.gz"

        main_src = tar.extractfile("projectA/main.src").read()
        assert main_src == b"caf\xc3\xa9\n", "projectA/main.src was not correctly converted to UTF-8."

        helper_src = tar.extractfile("projectA/utils/helper.src").read()
        assert helper_src == b"r\xc3\xa9sum\xc3\xa9\n", "projectA/utils/helper.src was not correctly converted to UTF-8."

        readme = tar.extractfile("projectA/readme.txt").read()
        assert readme == b"README\n", "projectA/readme.txt was modified but should have been left untouched."

    # Check legacy_code_B.tar.gz
    with tarfile.open(archive_b, "r:gz") as tar:
        members = tar.getnames()
        assert "moduleB/app.src" in members, "moduleB/app.src missing in legacy_code_B.tar.gz"

        app_src = tar.extractfile("moduleB/app.src").read()
        assert app_src == b"ni\xc3\xb1o\n", "moduleB/app.src was not correctly converted to UTF-8."