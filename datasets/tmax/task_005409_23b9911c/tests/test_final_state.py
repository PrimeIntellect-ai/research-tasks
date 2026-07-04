# test_final_state.py

import os
import json
import tarfile
import pytest

def test_summary_json():
    summary_path = "/home/user/summary.json"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} does not exist."

    with open(summary_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    assert "links_created" in data, "Key 'links_created' missing in summary.json"
    assert "tmp_deleted" in data, "Key 'tmp_deleted' missing in summary.json"
    assert data["links_created"] == 2, f"Expected 2 links_created, got {data['links_created']}"
    assert data["tmp_deleted"] == 4, f"Expected 4 tmp_deleted, got {data['tmp_deleted']}"

def test_hard_links_created():
    file1 = "/home/user/data/file1.txt"
    file2 = "/home/user/data/file2.txt"
    file3 = "/home/user/data/dirA/file3.txt"
    file4 = "/home/user/data/dirA/file4.txt"

    for f in [file1, file2, file3, file4]:
        assert os.path.isfile(f), f"Expected file {f} is missing."

    inode1 = os.stat(file1).st_ino
    inode2 = os.stat(file2).st_ino
    assert inode1 == inode2, f"Files {file1} and {file2} are not hard linked (different inodes)."

    inode3 = os.stat(file3).st_ino
    inode4 = os.stat(file4).st_ino
    assert inode3 == inode4, f"Files {file3} and {file4} are not hard linked (different inodes)."

def test_tmp_files_deleted():
    data_dir = "/home/user/data"
    assert os.path.isdir(data_dir), f"Directory {data_dir} is missing."

    tmp_files_found = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".tmp"):
                tmp_files_found.append(os.path.join(root, file))

    assert len(tmp_files_found) == 0, f"Found leftover .tmp files: {tmp_files_found}"

def test_archive_exists_and_valid():
    archive_path = "/home/user/data_archive.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()

            # Extract just the filenames to handle different ways tar might have been invoked (e.g. absolute vs relative paths)
            basenames = [os.path.basename(n) for n in names if not n.endswith('/')]

            expected_files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]
            for ef in expected_files:
                assert ef in basenames, f"Expected file {ef} is missing from the tar archive."

            # Ensure no .tmp files were archived
            for name in basenames:
                assert not name.endswith(".tmp"), f"Archived file {name} has a .tmp extension, which should have been deleted."
    except tarfile.ReadError:
        pytest.fail(f"Failed to read {archive_path} as a gzip-compressed tar archive.")