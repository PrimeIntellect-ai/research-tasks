# test_final_state.py

import os
import tarfile

def test_incremental_update_archive_exists_and_valid():
    archive_path = "/home/user/incremental_update.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} is missing."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

def test_incremental_update_archive_contents():
    archive_path = "/home/user/incremental_update.tar.gz"
    assert os.path.isfile(archive_path), "Archive is missing, cannot check contents."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            members = tar.getnames()
    except tarfile.ReadError:
        assert False, f"Failed to read {archive_path} as a gzipped tar archive."

    # Clean up names by removing leading './' and ignore directory entries if present
    cleaned_members = set(m.lstrip("./") for m in members)
    cleaned_members.discard("")  # in case './' becomes empty string

    expected_files = {"file2.txt", "file3.txt"}

    assert cleaned_members == expected_files, (
        f"Archive contents do not match expected incremental files.\n"
        f"Expected: {expected_files}\n"
        f"Got: {cleaned_members}"
    )