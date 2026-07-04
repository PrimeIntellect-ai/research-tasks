# test_final_state.py
import os
import glob

def test_executable_exists():
    path = "/home/user/log_archiver"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_archive_files_count_and_names():
    archive_dir = "/home/user/archives"
    assert os.path.isdir(archive_dir), f"Directory {archive_dir} does not exist."

    files = glob.glob(os.path.join(archive_dir, "archive_part_*.log"))
    assert len(files) == 3, f"Expected exactly 3 archive files, found {len(files)}."

    expected_files = [
        "archive_part_001.log",
        "archive_part_002.log",
        "archive_part_003.log"
    ]

    for expected in expected_files:
        expected_path = os.path.join(archive_dir, expected)
        assert os.path.isfile(expected_path), f"Expected archive file {expected_path} is missing."

def test_archive_files_content():
    archive_dir = "/home/user/archives"

    file1 = os.path.join(archive_dir, "archive_part_001.log")
    file2 = os.path.join(archive_dir, "archive_part_002.log")
    file3 = os.path.join(archive_dir, "archive_part_003.log")

    # Check lines count
    with open(file1, 'r') as f:
        lines1 = f.readlines()
    assert len(lines1) == 15, f"Expected 15 lines in {file1}, got {len(lines1)}."
    assert "Log entry 1:" in lines1[0], f"First line of {file1} is incorrect."
    assert "Log entry 15:" in lines1[-1], f"Last line of {file1} is incorrect."

    with open(file2, 'r') as f:
        lines2 = f.readlines()
    assert len(lines2) == 15, f"Expected 15 lines in {file2}, got {len(lines2)}."
    assert "Log entry 16:" in lines2[0], f"First line of {file2} is incorrect."
    assert "Log entry 30:" in lines2[-1], f"Last line of {file2} is incorrect."

    with open(file3, 'r') as f:
        lines3 = f.readlines()
    assert len(lines3) == 12, f"Expected 12 lines in {file3}, got {len(lines3)}."
    assert "Log entry 31:" in lines3[0], f"First line of {file3} is incorrect."
    assert "Log entry 42:" in lines3[-1], f"Last line of {file3} is incorrect."