# test_final_state.py

import os
import stat
import tarfile
import pytest

def test_pigz_compiled():
    """Verify that pigz has been compiled and is executable."""
    pigz_path = '/app/pigz-2.8/pigz'
    assert os.path.isfile(pigz_path), f"Compiled pigz binary not found at {pigz_path}."
    assert os.access(pigz_path, os.X_OK), f"pigz binary at {pigz_path} is not executable."

def test_script_exists_and_executable():
    """Verify that the process_logs.sh script exists and is executable."""
    script_path = '/home/user/process_logs.sh'
    assert os.path.isfile(script_path), f"Script not found at {script_path}."
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable."

def test_archive_exists():
    """Verify that the final archive was generated."""
    archive_path = '/home/user/final_archive.tar.gz'
    assert os.path.isfile(archive_path), f"Final archive not found at {archive_path}."

def test_archive_contents():
    """Verify that the archive contains exactly the valid WAL files."""
    archive_path = '/home/user/final_archive.tar.gz'
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, 'r:*') as tar:
        members = tar.getnames()

    # Extract just the basenames to be robust against how they were tarred (absolute vs relative)
    basenames = [os.path.basename(m) for m in members if os.path.basename(m).startswith('wal_')]

    expected_valid = [f"wal_{i:03d}.log" for i in range(1, 21)]
    expected_invalid = [f"wal_{i:03d}.log" for i in range(21, 36)]

    for valid_file in expected_valid:
        assert valid_file in basenames, f"Valid WAL file {valid_file} is missing from the archive."

    for invalid_file in expected_invalid:
        assert invalid_file not in basenames, f"Invalid WAL file {invalid_file} was incorrectly included in the archive."

    assert len(basenames) == len(expected_valid), f"Archive contains an unexpected number of WAL files. Expected {len(expected_valid)}, got {len(basenames)}."

def test_archive_size_metric():
    """Verify that the final archive size meets the metric threshold."""
    archive_path = '/home/user/final_archive.tar.gz'
    assert os.path.isfile(archive_path), f"Final archive not found at {archive_path}."

    file_size = os.path.getsize(archive_path)
    threshold = 500000

    assert file_size <= threshold, (
        f"Archive size metric failed: {file_size} bytes is not <= {threshold} bytes. "
        "Ensure you are filtering invalid files and using maximum compression (-9)."
    )