# test_final_state.py

import os
import tarfile
import pytest

def test_organized_data_directory():
    organized_dir = "/home/user/organized_data"
    assert os.path.isdir(organized_dir), f"Directory {organized_dir} does not exist."

    files = set(os.listdir(organized_dir))
    expected_files = {
        "TUN_reading_01.tar.gz",
        "GLA_reading_02.zip",
        "OCE_reading_03.tar.gz"
    }

    assert files == expected_files, f"Expected files {expected_files} in {organized_dir}, but found {files}."

def test_final_dataset_archive():
    archive_path = "/home/user/final_dataset.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
    except tarfile.TarError:
        pytest.fail(f"File {archive_path} is not a valid tar.gz archive.")

    # Check that the archive contains the organized_data directory and the 3 files
    # The exact paths in the tar might vary (e.g., "organized_data/..." or "/home/user/organized_data/..."), 
    # so we'll check for the basenames of the expected files.
    basenames = {os.path.basename(name) for name in names if not name.endswith('/')}
    expected_basenames = {
        "TUN_reading_01.tar.gz",
        "GLA_reading_02.zip",
        "OCE_reading_03.tar.gz"
    }

    missing = expected_basenames - basenames
    assert not missing, f"Archive {archive_path} is missing expected files: {missing}"

def test_processing_log():
    log_path = "/home/user/processing_log.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/raw_data/site_A/2021/reading_01.tar.gz -> TUN_reading_01.tar.gz",
        "/home/user/raw_data/site_A/2022/reading_02.zip -> GLA_reading_02.zip",
        "/home/user/raw_data/site_B/logs/reading_03.tar.gz -> OCE_reading_03.tar.gz"
    ]

    assert lines == expected_lines, (
        f"Log file contents do not match expected sorted output.\n"
        f"Expected:\n{expected_lines}\n"
        f"Got:\n{lines}"
    )