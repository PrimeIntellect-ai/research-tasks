# test_final_state.py
import os
import tarfile
import pytest

def test_files_moved_and_renamed():
    organized_dir = "/home/user/recovery/organized"

    expected_files = [
        "file1.png",
        "file2.pdf",
        "file3.txt",
        "file4.gz"
    ]

    for f in expected_files:
        path = os.path.join(organized_dir, f)
        assert os.path.isfile(path), f"Expected file {path} is missing. Make sure files were moved and renamed correctly."

def test_tar_archive_exists_and_contents():
    tar_path = "/home/user/backup_incr.tar"
    assert os.path.isfile(tar_path), f"Tar archive {tar_path} is missing."

    try:
        with tarfile.open(tar_path, "r") as tar:
            members = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"File {tar_path} is not a valid tar archive.")

    assert "file1.png" not in members, "file1.png should not be in the archive because it is older than the backup stamp."

    expected_members = {"file2.pdf", "file3.txt", "file4.gz"}
    actual_members = set(members)

    assert actual_members == expected_members, (
        f"Archive contents do not match expected.\n"
        f"Expected exactly: {expected_members}\n"
        f"Got: {actual_members}\n"
        f"Ensure no leading directories are included in the tar archive."
    )