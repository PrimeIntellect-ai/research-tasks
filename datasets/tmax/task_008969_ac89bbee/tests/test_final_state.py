# test_final_state.py

import os
import hashlib
import pytest

def test_pipeline_files_exist():
    assert os.path.isfile("/home/user/pipeline.c"), "The source file /home/user/pipeline.c does not exist."
    assert os.path.isfile("/home/user/run.sh"), "The script /home/user/run.sh does not exist."
    assert os.path.isfile("/home/user/pipeline"), "The compiled executable /home/user/pipeline does not exist."

def test_recommendations_csv_content():
    file_path = "/home/user/output/recommendations.csv"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    expected_lines = [
        "id,nearest_neighbor_id",
        "1,4",
        "2,1",
        "3,5",
        "4,1",
        "5,3",
        "6,7",
        "7,6"
    ]

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"The contents of {file_path} do not match the expected recommendations."

def test_checksum_file():
    checksum_path = "/home/user/output/checksum.txt"
    recs_path = "/home/user/output/recommendations.csv"

    assert os.path.isfile(checksum_path), f"The file {checksum_path} does not exist."
    assert os.path.isfile(recs_path), f"The file {recs_path} does not exist."

    with open(recs_path, "rb") as f:
        file_bytes = f.read()

    expected_hash = hashlib.sha256(file_bytes).hexdigest()

    with open(checksum_path, "r") as f:
        checksum_content = f.read().strip()

    # The checksum file should contain the hash, likely followed by the filename (run1.csv)
    assert checksum_content.startswith(expected_hash), f"{checksum_path} does not contain the correct SHA256 hash."
    assert "run1.csv" in checksum_content, f"{checksum_path} does not seem to have been generated from 'run1.csv'."