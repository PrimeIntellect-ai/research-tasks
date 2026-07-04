# test_final_state.py

import os
import tarfile
import pytest

def test_csv_exists_and_content():
    csv_path = "/home/user/valid_artifacts.csv"
    assert os.path.isfile(csv_path), f"{csv_path} does not exist."

    with open(csv_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in CSV (header + 2 valid artifacts), found {len(lines)}."

    assert lines[0] == "Filename,Magic,Description", "CSV header is incorrect."
    assert lines[1] == "file1.bin,CAFEBABE,First valid file", "First valid artifact entry is incorrect."
    assert lines[2] == "file3.bin,12345678,Third valid file with special char: É", "Second valid artifact entry is incorrect or not properly UTF-8 encoded."

def test_tar_gz_exists_and_content():
    tar_path = "/home/user/curated.tar.gz"
    assert os.path.isfile(tar_path), f"{tar_path} does not exist."

    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar archive."

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getnames()

    # Should contain exactly file1.bin and file3.bin at the root
    expected_members = {"file1.bin", "file3.bin"}
    actual_members = set(members)

    assert actual_members == expected_members, f"Archive contents mismatch. Expected {expected_members}, found {actual_members}. Make sure there are no directory paths."