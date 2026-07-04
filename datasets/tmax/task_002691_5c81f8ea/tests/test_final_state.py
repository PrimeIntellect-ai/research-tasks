# test_final_state.py

import os
import tarfile
import pytest

RESTORED_ARCHIVE = "/home/user/restored_backups.tar.gz"

EXPECTED_FILES = {
    "Alpha77.log": "ID: Alpha77",
    "Bravo88.log": "ID: Bravo88",
    "Charlie99.log": "ID: Charlie99"
}

def test_restored_archive_exists():
    """Check if the restored archive exists."""
    assert os.path.isfile(RESTORED_ARCHIVE), f"{RESTORED_ARCHIVE} does not exist."

def test_restored_archive_is_valid_tar_gz():
    """Check if the restored archive is a valid gzip-compressed tarball."""
    assert os.path.isfile(RESTORED_ARCHIVE), f"{RESTORED_ARCHIVE} does not exist."
    assert tarfile.is_tarfile(RESTORED_ARCHIVE), f"{RESTORED_ARCHIVE} is not a valid tar archive."

    # Try opening it with 'r:gz' to ensure it's gzip compressed
    try:
        with tarfile.open(RESTORED_ARCHIVE, "r:gz") as tar:
            pass
    except tarfile.ReadError:
        pytest.fail(f"{RESTORED_ARCHIVE} is not a valid gzip-compressed tarball.")

def test_restored_archive_contents():
    """Check if the restored archive contains the correct files with correct content."""
    assert os.path.isfile(RESTORED_ARCHIVE), f"{RESTORED_ARCHIVE} does not exist."

    try:
        with tarfile.open(RESTORED_ARCHIVE, "r:gz") as tar:
            members = tar.getmembers()

            # Check that only files are present (no directories or other types)
            # and that they are at the root level (no slashes in names)
            actual_filenames = []
            for m in members:
                assert m.isfile(), f"Archive contains non-file member: {m.name}"
                # Remove any leading './' that tar might add
                name = m.name.lstrip('./')
                assert '/' not in name, f"File {name} is not at the root level of the archive."
                actual_filenames.append(name)

            # Check exactly the expected files
            assert set(actual_filenames) == set(EXPECTED_FILES.keys()), \
                f"Archive contains incorrect files. Expected {set(EXPECTED_FILES.keys())}, found {set(actual_filenames)}"

            # Check contents and encoding
            for filename, expected_first_line in EXPECTED_FILES.items():
                # Find the actual member name in the archive
                member_name = next(m.name for m in members if m.name.lstrip('./') == filename)
                f = tar.extractfile(member_name)
                assert f is not None, f"Could not read {filename} from archive."

                raw_content = f.read()
                try:
                    text_content = raw_content.decode('utf-8')
                except UnicodeDecodeError:
                    pytest.fail(f"File {filename} is not valid UTF-8 encoded.")

                lines = text_content.splitlines()
                assert len(lines) > 0, f"File {filename} is empty."
                assert lines[0] == expected_first_line, \
                    f"First line of {filename} is '{lines[0]}', expected '{expected_first_line}'"

    except tarfile.ReadError:
        pytest.fail(f"Failed to read {RESTORED_ARCHIVE}.")