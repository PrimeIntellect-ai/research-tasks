# test_final_state.py

import os
import tarfile
import json
import pytest

SUMMARY_FILE = "/home/user/summary.txt"
TARBALL_FILE = "/home/user/clean_configs.tar.gz"

EXPECTED_FILES = [
    "archive1_valid2.json",
    "loose_valid1.json"
]

def test_summary_file_exists_and_correct():
    assert os.path.isfile(SUMMARY_FILE), f"The summary file {SUMMARY_FILE} is missing."

    with open(SUMMARY_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == EXPECTED_FILES, (
        f"The contents of {SUMMARY_FILE} do not match the expected list of valid JSON files.\n"
        f"Expected: {EXPECTED_FILES}\n"
        f"Found: {lines}"
    )

def test_tarball_exists_and_contains_correct_files():
    assert os.path.isfile(TARBALL_FILE), f"The tarball {TARBALL_FILE} is missing."
    assert tarfile.is_tarfile(TARBALL_FILE), f"The file {TARBALL_FILE} is not a valid tar archive."

    with tarfile.open(TARBALL_FILE, "r:gz") as tar:
        members = tar.getmembers()

        # Check that all members are regular files
        for member in members:
            assert member.isfile(), f"Tarball contains non-file member: {member.name}"

        # Extract base filenames, removing any './' prefix or directory paths
        filenames = sorted([os.path.basename(member.name) for member in members])

        assert filenames == EXPECTED_FILES, (
            f"The tarball {TARBALL_FILE} does not contain the exact expected valid JSON files.\n"
            f"Expected: {EXPECTED_FILES}\n"
            f"Found: {filenames}"
        )

def test_tarball_files_are_valid_json():
    # Double check that the files inside the tarball are actually valid JSON
    with tarfile.open(TARBALL_FILE, "r:gz") as tar:
        for member in tar.getmembers():
            f = tar.extractfile(member)
            assert f is not None, f"Could not extract {member.name} from tarball."
            content = f.read().decode('utf-8')
            try:
                json.loads(content)
            except json.JSONDecodeError:
                pytest.fail(f"File {member.name} inside the tarball is not valid JSON.")