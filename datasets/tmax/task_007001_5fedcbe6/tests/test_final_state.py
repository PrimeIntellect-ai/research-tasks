# test_final_state.py

import os
import tarfile
import pytest

def test_corrupted_log():
    log_path = "/home/user/corrupted.log"
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "/home/user/staging_repo/batch1/broken.tar.gz",
        "/home/user/staging_repo/batch2/bad_data.zip"
    ]

    assert lines == expected, f"Contents of {log_path} are incorrect. Expected {expected}, got {lines}."

def test_curated_release_tarball():
    tar_path = "/home/user/curated_release.tar.gz"
    assert os.path.exists(tar_path), f"{tar_path} does not exist."
    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar archive."

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            members = tar.getmembers()
            file_names = sorted([m.name for m in members if m.isfile()])

            expected_names = ["large_v1.bin", "large_v2.bin", "large_v3.bin"]
            assert file_names == expected_names, f"Tarball does not contain the exact expected files. Expected {expected_names}, got {file_names}."

            for m in members:
                if m.isfile():
                    assert m.size > 100000, f"File {m.name} in tarball has size {m.size}, which is not strictly greater than 100,000 bytes."
                    assert "/" not in m.name and "\\" not in m.name, f"File {m.name} is not at the root level of the tarball."
    except tarfile.ReadError:
        pytest.fail(f"{tar_path} could not be read as a gzip-compressed tarball.")

def test_extracted_staging_directory():
    staging_path = "/home/user/extracted_staging"
    assert os.path.isdir(staging_path), f"{staging_path} directory was not created or is not a directory."