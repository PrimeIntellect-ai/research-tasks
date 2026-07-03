# test_final_state.py

import os
import tarfile
import pytest

EXTRACTED_CONFIGS_PATH = "/home/user/extracted_configs.txt"
ARCHIVE_PATH = "/home/user/backup.tar.gz"

EXPECTED_CONFIGS = [
    "MAX_CONNECTIONS=500",
    "ENABLE_LOGGING=true",
    "CACHE_SIZE=1024MB"
]

def test_extracted_configs():
    assert os.path.isfile(EXTRACTED_CONFIGS_PATH), f"Extracted configs file {EXTRACTED_CONFIGS_PATH} does not exist."

    with open(EXTRACTED_CONFIGS_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == EXPECTED_CONFIGS, f"Extracted configs do not match expected. Got: {lines}, Expected: {EXPECTED_CONFIGS}"

def test_archive_exists_and_valid():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} does not exist."
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"File {ARCHIVE_PATH} is not a valid tar archive."

def test_archive_contents():
    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        members = tar.getnames()

    expected_members = {"backup_config.json", "extracted_configs.txt"}
    actual_members = set(members)

    assert actual_members == expected_members, f"Archive contents do not match expected root files. Got: {actual_members}, Expected: {expected_members}"