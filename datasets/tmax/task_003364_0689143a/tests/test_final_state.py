# test_final_state.py

import os
import json

def test_archive_report():
    report_path = "/home/user/archive_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["snap_101.bin", "snap_104.bin"]
    assert lines == expected_lines, f"Expected {expected_lines} in report, but got {lines}."

def test_hard_links():
    archive_dir = "/home/user/archive"
    source_dir = "/home/user/data/snapshots"

    assert os.path.isdir(archive_dir), f"Archive directory {archive_dir} does not exist."

    expected_files = ["snap_101.bin", "snap_104.bin"]

    for filename in expected_files:
        archive_path = os.path.join(archive_dir, filename)
        source_path = os.path.join(source_dir, filename)

        assert os.path.isfile(archive_path), f"Archived file {archive_path} does not exist."

        # Check hard link (same inode on the same device)
        archive_stat = os.stat(archive_path)
        source_stat = os.stat(source_path)

        assert archive_stat.st_dev == source_stat.st_dev, f"{archive_path} and {source_path} are not on the same device."
        assert archive_stat.st_ino == source_stat.st_ino, f"{archive_path} is not a hard link to {source_path}."

def test_no_extra_files():
    archive_dir = "/home/user/archive"
    assert os.path.isdir(archive_dir), f"Archive directory {archive_dir} does not exist."

    expected_files = {"snap_101.bin", "snap_104.bin"}
    actual_files = set(os.listdir(archive_dir))

    extra_files = actual_files - expected_files
    assert not extra_files, f"Found unexpected files in archive directory: {extra_files}"