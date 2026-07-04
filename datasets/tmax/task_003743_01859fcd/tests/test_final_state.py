# test_final_state.py

import os
import tarfile

EXPECTED_CONTENT = """Status: PUBLISHED

# API V2
These are the new API docs.
Use the endpoints carefully.
Status: PUBLISHED

# Setup Guide
Run the installer to begin.
"""

def test_release_manual_content():
    manual_path = "/home/user/release_manual.md"
    assert os.path.isfile(manual_path), f"Expected file {manual_path} does not exist."

    with open(manual_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.strip() == EXPECTED_CONTENT.strip(), "The contents of release_manual.md do not match the expected output."

def test_release_archive_exists_and_contains_manual():
    archive_path = "/home/user/release.tar.gz"
    assert os.path.isfile(archive_path), f"Expected archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"The file {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()
        # Check if release_manual.md is in the archive (allowing for paths like ./release_manual.md or /home/user/release_manual.md)
        found = any(m.endswith("release_manual.md") for m in members)
        assert found, f"The archive {archive_path} does not contain release_manual.md. Contents: {members}"