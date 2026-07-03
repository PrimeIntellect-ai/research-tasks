# test_final_state.py
import os
import re
import tarfile
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_backups.py"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_log_file_and_archive_validity():
    log_path = "/home/user/backup_summary.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Log file should have exactly 3 non-empty lines, found {len(lines)}"

    # Check Mount
    expected_mount = "/home/user/mnt/remote_backups"
    assert lines[0] == f"Mount: {expected_mount}", f"Line 1 incorrect. Expected 'Mount: {expected_mount}', got '{lines[0]}'"

    # Check Size
    cfg_dir = "/home/user/router_configs"
    expected_size = 0
    for file in os.listdir(cfg_dir):
        if file.endswith(".cfg"):
            expected_size += os.path.getsize(os.path.join(cfg_dir, file))

    assert lines[1] == f"Size: {expected_size}", f"Line 2 incorrect. Expected 'Size: {expected_size}', got '{lines[1]}'"

    # Check Archive
    archive_line = lines[2]
    assert archive_line.startswith("Archive: "), f"Line 3 should start with 'Archive: ', got '{archive_line}'"
    archive_path = archive_line[len("Archive: "):].strip()

    pattern = r"^/home/user/mnt/remote_backups/backup_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_tokyo\.tar\.gz$"
    assert re.match(pattern, archive_path), f"Archive path format incorrect: {archive_path}"

    assert os.path.isfile(archive_path), f"Archive file does not exist at {archive_path}"

    # Verify tarball contents
    assert tarfile.is_tarfile(archive_path), f"File is not a valid tar archive: {archive_path}"

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()

        # Check that cfg files are in the archive
        cfg_files_in_dir = [f for f in os.listdir(cfg_dir) if f.endswith(".cfg")]
        for cfg in cfg_files_in_dir:
            # The files might be stored with or without paths, but their basenames should be present
            assert any(cfg in name for name in names), f"Expected config file {cfg} not found in archive"

        # Check that readme.txt is NOT in the archive
        assert not any("readme.txt" in name for name in names), "readme.txt should not be included in the archive"