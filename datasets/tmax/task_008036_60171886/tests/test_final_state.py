# test_final_state.py

import os
import tarfile
import pytest

def test_extracted_project_exists():
    path = "/home/user/extracted_project/project"
    assert os.path.isdir(path), f"Directory {path} does not exist. The archive was not extracted correctly."

def test_final_index_txt():
    path = "/home/user/final_index.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/extracted_project/project/dirA/file2.txt 11",
        "/home/user/extracted_project/project/file1.txt 11"
    ]

    assert lines == expected_lines, f"Contents of {path} do not match the expected unique files and sizes."

def test_clean_backup_tar():
    path = "/home/user/clean_backup.tar"
    assert os.path.isfile(path), f"Archive {path} does not exist."

    try:
        with tarfile.open(path, "r") as tar:
            names = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"File {path} is not a valid tar archive.")

    # Tar might strip leading slashes, so we normalize for comparison
    normalized_names = [name.lstrip('/') for name in names]

    expected_files = [
        "home/user/extracted_project/project/dirA/file2.txt",
        "home/user/extracted_project/project/file1.txt"
    ]

    # Check that exactly the expected files are in the tar (ignoring directories if any are implicitly added, but the prompt says "contains exactly those two files")
    # To be robust, we filter out directories if they exist, or just check that the expected files are present and no other regular files.
    file_members = [m.name.lstrip('/') for m in tar.getmembers() if m.isfile()]

    assert sorted(file_members) == sorted(expected_files), f"The archive {path} does not contain the exact expected files."