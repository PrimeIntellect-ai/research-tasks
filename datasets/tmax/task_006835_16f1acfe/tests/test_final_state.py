# test_final_state.py

import os
import tarfile
import gzip
import pytest

def test_c_source_exists():
    assert os.path.isfile("/home/user/filter_logs.c"), "/home/user/filter_logs.c is missing."

def test_executable_exists():
    exe_path = "/home/user/filter_logs"
    assert os.path.isfile(exe_path), f"{exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_archived_list_contents():
    list_path = "/home/user/archived_list.txt"
    assert os.path.isfile(list_path), f"{list_path} is missing."

    with open(list_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_files = {
        "/home/user/logs/app1/error.log",
        "/home/user/logs/app2/crash.log",
        "/home/user/logs/db/corruption.log"
    }

    actual_files = set(lines)
    assert actual_files == expected_files, f"Contents of {list_path} do not match expected files. Expected {expected_files}, got {actual_files}."
    assert len(lines) == len(expected_files), f"Duplicates found or incorrect number of lines in {list_path}."

def test_tarball_exists_and_valid():
    tar_path = "/home/user/cold_storage.tar.gz"
    assert os.path.isfile(tar_path), f"{tar_path} is missing."

    try:
        with gzip.open(tar_path, "rb") as f:
            f.read(1)
    except Exception as e:
        pytest.fail(f"{tar_path} is not a valid gzip file: {e}")

def test_tarball_contents():
    tar_path = "/home/user/cold_storage.tar.gz"
    assert os.path.isfile(tar_path), f"{tar_path} is missing."

    expected_files = {
        "/home/user/logs/app1/error.log",
        "/home/user/logs/app2/crash.log",
        "/home/user/logs/db/corruption.log"
    }

    # Tar might store paths with or without leading slash
    expected_files_stripped = {f.lstrip("/") for f in expected_files}

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            members = tar.getnames()
    except Exception as e:
        pytest.fail(f"Failed to read tarball contents: {e}")

    actual_files_stripped = {m.lstrip("/") for m in members}

    assert actual_files_stripped == expected_files_stripped, (
        f"Tarball contents do not match expected files. "
        f"Expected {expected_files_stripped}, got {actual_files_stripped}."
    )