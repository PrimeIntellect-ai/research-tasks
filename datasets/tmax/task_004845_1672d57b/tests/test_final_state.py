# test_final_state.py

import os
import pytest

OUTPUT_FILE = "/home/user/bad_commit.txt"
EXPECTED_SHA_FILE = "/tmp/expected_bad_commit.txt"

def test_bad_commit_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"The required output file {OUTPUT_FILE} does not exist. Did you save the commit SHA?"

def test_bad_commit_sha_matches():
    assert os.path.isfile(EXPECTED_SHA_FILE), f"Expected SHA file {EXPECTED_SHA_FILE} is missing from the environment."

    with open(OUTPUT_FILE, 'r') as f:
        student_sha = f.read().strip()

    with open(EXPECTED_SHA_FILE, 'r') as f:
        expected_sha = f.read().strip()

    assert student_sha != "", "The output file is empty."
    assert student_sha == expected_sha, f"The SHA provided ({student_sha}) does not match the actual bad commit ({expected_sha})."