# test_final_state.py
import os
import tarfile
import pytest

def test_get_header_c_exists():
    path = "/home/user/get_header.c"
    assert os.path.isfile(path), f"Source file {path} is missing. You must write the C program here."

def test_get_header_executable():
    path = "/home/user/get_header"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the C program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_manifest_content():
    path = "/home/user/manifest.txt"
    assert os.path.isfile(path), f"Manifest file {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "DE AD BE EF 00 00 00 01 /vault/archive/file1.arc",
        "CA FE BA BE 00 00 00 02 /vault/archive/file2.arc"
    ]

    assert lines == expected_lines, (
        f"Manifest content is incorrect.\n"
        f"Expected:\n{expected_lines}\n"
        f"Got:\n{lines}\n"
        "Ensure you matched the right files, formatted the hex headers properly, "
        "transformed the paths, and sorted alphabetically."
    )

def test_tar_content():
    path = "/home/user/inc_backup.tar"
    assert os.path.isfile(path), f"Tar archive {path} is missing."

    try:
        with tarfile.open(path, "r") as tar:
            members = sorted(tar.getnames())
    except tarfile.ReadError:
        pytest.fail(f"File {path} is not a valid tar archive.")

    expected_members = ["file1.arc", "file2.arc"]
    assert members == expected_members, (
        f"Tar archive contents are incorrect.\n"
        f"Expected exactly these relative paths: {expected_members}\n"
        f"Got: {members}"
    )