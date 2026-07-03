# test_final_state.py

import os
import tarfile
import tempfile
import pytest

FINAL_TARBALL = "/home/user/final_docs.tar.gz"
EXTRACTED_DIR = "/home/user/extracted"

def test_final_tarball_exists():
    assert os.path.exists(FINAL_TARBALL), f"The final archive {FINAL_TARBALL} does not exist."
    assert os.path.isfile(FINAL_TARBALL), f"{FINAL_TARBALL} is not a file."

def test_final_tarball_contents():
    assert os.path.exists(FINAL_TARBALL), f"The final archive {FINAL_TARBALL} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(FINAL_TARBALL, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        extracted_files = set(os.listdir(tmpdir))

        expected_files = {"intro.md", "api_reference.md", "troubleshooting.md"}

        # Check that all expected files are present
        for expected in expected_files:
            assert expected in extracted_files, f"Expected file '{expected}' is missing from the tarball."

        # Check that no file has the 'Draft_v' prefix
        for file in extracted_files:
            assert not file.startswith("Draft_"), f"File '{file}' in tarball still has the 'Draft_' prefix."

        # Check content of troubleshooting.md
        troubleshooting_path = os.path.join(tmpdir, "troubleshooting.md")
        with open(troubleshooting_path, "r") as f:
            content = f.read()
            assert "Have you tried turning it off and on again?" in content, \
                f"Content of troubleshooting.md is incorrect. Got: {content}"

def test_extracted_directory_exists():
    assert os.path.exists(EXTRACTED_DIR), f"The directory {EXTRACTED_DIR} does not exist."
    assert os.path.isdir(EXTRACTED_DIR), f"{EXTRACTED_DIR} is not a directory."