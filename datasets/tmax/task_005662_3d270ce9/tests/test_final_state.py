# test_final_state.py

import os
import tarfile
import pytest

ARCHIVE_PATH = "/home/user/backup/docs_diff.tar.gz"
EXPECTED_FILES = {"doc_015.txt", "doc_042.txt", "doc_088.txt", "doc_101.txt", "doc_102.txt"}

def test_archive_exists():
    """Verify that the differential backup archive exists."""
    assert os.path.isfile(ARCHIVE_PATH), f"Archive not found at {ARCHIVE_PATH}"

def test_archive_is_valid_tar_gz():
    """Verify that the archive is a valid gzipped tarball."""
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"File {ARCHIVE_PATH} is not a valid tar archive."

    # Also verify it can be opened with gzip compression
    try:
        with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
            pass
    except Exception as e:
        pytest.fail(f"Could not open archive as a gzip-compressed tarball: {e}")

def test_archive_contents():
    """Verify that the archive contains exactly the expected modified and new files."""
    try:
        with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
            members = tar.getmembers()
    except Exception as e:
        pytest.fail(f"Failed to read archive contents: {e}")

    # Extract just the basenames of the files in the tarball
    # We ignore directories or other non-file entries, though the task implies only files
    actual_files = set()
    for member in members:
        if member.isfile():
            basename = os.path.basename(member.name)
            if basename.endswith(".txt"):
                actual_files.add(basename)

    assert actual_files == EXPECTED_FILES, (
        f"Archive contents do not match expected files.\n"
        f"Expected: {sorted(EXPECTED_FILES)}\n"
        f"Found: {sorted(actual_files)}"
    )