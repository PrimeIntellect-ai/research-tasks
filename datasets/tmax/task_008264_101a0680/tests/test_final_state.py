# test_final_state.py

import os
import tarfile
import csv
import pytest

WORKSPACE_DIR = "/home/user/workspace"
RAW_DATA_DIR = os.path.join(WORKSPACE_DIR, "raw_data")
ORGANIZED_DIR = os.path.join(WORKSPACE_DIR, "organized")
ARCHIVE_PATH = os.path.join(WORKSPACE_DIR, "archive.tar.gz")

def test_organized_directory_structure():
    assert os.path.isdir(ORGANIZED_DIR), f"Missing directory: {ORGANIZED_DIR}"
    assert os.path.isdir(os.path.join(ORGANIZED_DIR, "datasets")), "Missing datasets directory"
    assert os.path.isdir(os.path.join(ORGANIZED_DIR, "binaries", "x86_64")), "Missing binaries/x86_64 directory"
    assert os.path.isdir(os.path.join(ORGANIZED_DIR, "binaries", "other")), "Missing binaries/other directory"
    assert os.path.isdir(os.path.join(ORGANIZED_DIR, "logs")), "Missing logs directory"

def test_datasets_processed():
    data1_path = os.path.join(ORGANIZED_DIR, "datasets", "data1.csv")
    data2_path = os.path.join(ORGANIZED_DIR, "datasets", "data2.csv")

    assert os.path.isfile(data1_path), f"Missing file: {data1_path}"
    assert os.path.isfile(data2_path), f"Missing file: {data2_path}"

    def check_csv(filepath, expected_rows):
        with open(filepath, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == expected_rows, f"{filepath} has incorrect number of data rows."
            for row in rows:
                assert row.get('status') != 'ERROR', f"Found ERROR row in {filepath}"

    # data1.csv originally has 4 rows (1 header + 3 data). 2 are ERROR. Expected data rows: 2
    check_csv(data1_path, 2)
    # data2.csv originally has 4 rows (1 header + 3 data). 1 is ERROR. Expected data rows: 2
    check_csv(data2_path, 2)

def test_binaries_hardlinked():
    worker_orig = os.path.join(RAW_DATA_DIR, "worker")
    worker_link = os.path.join(ORGANIZED_DIR, "binaries", "x86_64", "worker")

    dummy_orig = os.path.join(RAW_DATA_DIR, "dummy_arm")
    dummy_link = os.path.join(ORGANIZED_DIR, "binaries", "other", "dummy_arm")

    assert os.path.isfile(worker_link), f"Missing file: {worker_link}"
    assert os.path.isfile(dummy_link), f"Missing file: {dummy_link}"

    stat_orig_worker = os.stat(worker_orig)
    stat_link_worker = os.stat(worker_link)
    assert stat_orig_worker.st_ino == stat_link_worker.st_ino, "worker is not a hardlink to the original file"

    stat_orig_dummy = os.stat(dummy_orig)
    stat_link_dummy = os.stat(dummy_link)
    assert stat_orig_dummy.st_ino == stat_link_dummy.st_ino, "dummy_arm is not a hardlink to the original file"

def test_logs_symlinked():
    sys_orig = os.path.join(RAW_DATA_DIR, "sys.log")
    sys_link = os.path.join(ORGANIZED_DIR, "logs", "sys.log")

    debug_orig = os.path.join(RAW_DATA_DIR, "debug.log")
    debug_link = os.path.join(ORGANIZED_DIR, "logs", "debug.log")

    for link_path, orig_path in [(sys_link, sys_orig), (debug_link, debug_orig)]:
        assert os.path.islink(link_path), f"Not a symlink: {link_path}"
        target = os.readlink(link_path)
        abs_target = os.path.abspath(os.path.join(os.path.dirname(link_path), target))
        assert abs_target == orig_path, f"Symlink {link_path} does not point to {orig_path}"

def test_archive_created_and_valid():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive missing: {ARCHIVE_PATH}"

    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        members = tar.getmembers()
        paths = [m.name for m in members]

        # Check if the organized directory is at the root or nested, but we just check suffix matches
        assert any(p.endswith("datasets/data1.csv") for p in paths), "data1.csv missing from archive"
        assert any(p.endswith("binaries/x86_64/worker") for p in paths), "worker missing from archive"
        assert any(p.endswith("logs/sys.log") for p in paths), "sys.log missing from archive"

        # Verify symlinks are preserved in the archive
        sys_log_members = [m for m in members if m.name.endswith("logs/sys.log")]
        assert sys_log_members, "sys.log not found in tarball"
        assert sys_log_members[0].issym(), "sys.log is not a symlink in the tarball"