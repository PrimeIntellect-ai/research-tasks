# test_final_state.py

import os
import tarfile
import pytest

def test_pipeline_script_exists():
    assert os.path.isfile("/home/user/pipeline.sh"), "The pipeline script /home/user/pipeline.sh does not exist."
    assert os.access("/home/user/pipeline.sh", os.X_OK), "The pipeline script /home/user/pipeline.sh is not executable."

def test_top_similar_output():
    output_path = "/home/user/output/top_similar.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_users = ["U005", "U002", "U004"]
    assert lines == expected_users, f"Expected top similar users to be {expected_users}, but got {lines}."

def test_correlation_output():
    output_path = "/home/user/output/correlation.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "-0.806", f"Expected correlation to be '-0.806', but got '{content}'."

def test_archive_exists_and_valid():
    archive_path = "/home/user/archive/data_archive.tar.gz"
    assert os.path.isfile(archive_path), f"The archive file {archive_path} does not exist."

    assert tarfile.is_tarfile(archive_path), f"The file {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()
        # Check if user_features.csv is in the archive (it might be under a directory path)
        found = any("user_features.csv" in member for member in members)
        assert found, f"The archive {archive_path} does not contain 'user_features.csv'. Members found: {members}"