# test_final_state.py

import os
import tarfile
import pytest

def test_corruption_log():
    log_path = "/home/user/corruption.log"
    assert os.path.isfile(log_path), f"Corruption log is missing at {log_path}"
    with open(log_path, "r") as f:
        content = f.read()
    assert "719" in content, "Corruption log does not mention the corrupted artifact ID 719"

def test_curated_release_archive():
    archive_path = "/home/user/curated_release.tar.xz"
    assert os.path.isfile(archive_path), f"Final archive is missing at {archive_path}"

    # Check the file size metric
    file_size = os.path.getsize(archive_path)
    threshold = 5000
    assert file_size <= threshold, f"Archive size {file_size} bytes exceeds the maximum allowed size of {threshold} bytes. Use stronger compression."

    # Check the contents of the archive
    try:
        with tarfile.open(archive_path, "r:xz") as tar:
            members = tar.getmembers()
            # Filter out directories if any, and get base names
            file_names = [os.path.basename(m.name) for m in members if m.isfile()]
    except Exception as e:
        pytest.fail(f"Failed to open the archive {archive_path} as a tar.xz file: {e}")

    expected_files = {"release_105_stable.bin", "release_302_stable.bin", "release_884_stable.bin"}
    actual_files = set(file_names)

    assert actual_files == expected_files, f"Archive contents do not match expected files. Expected {expected_files}, got {actual_files}"