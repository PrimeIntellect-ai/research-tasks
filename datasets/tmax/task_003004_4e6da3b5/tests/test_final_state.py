# test_final_state.py

import os
import tarfile
import pytest

def test_extracted_directories():
    """Verify that only successful builds were extracted."""
    success_101 = "/home/user/curated/build_101"
    success_103 = "/home/user/curated/build_103"
    failure_102 = "/home/user/curated/build_102"
    failure_104 = "/home/user/curated/build_104"

    assert os.path.isdir(success_101), f"Expected extracted directory missing: {success_101}"
    assert os.path.isdir(success_103), f"Expected extracted directory missing: {success_103}"

    assert not os.path.exists(failure_102), f"Failed build should not have been extracted: {failure_102}"
    assert not os.path.exists(failure_104), f"Failed build should not have been extracted: {failure_104}"

def test_latest_symlink():
    """Verify the 'latest' symlink points to the highest successful build directory name."""
    symlink_path = "/home/user/curated/latest"

    assert os.path.islink(symlink_path), f"Expected a symbolic link at {symlink_path}"

    target = os.readlink(symlink_path)
    expected_target = "build_103"

    assert target == expected_target, f"Symlink points to '{target}' instead of '{expected_target}'"

def test_hardlinks_created():
    """Verify that identical files across builds share the same inode."""
    file1 = "/home/user/curated/build_101/lib.so"
    file2 = "/home/user/curated/build_103/lib.so"

    assert os.path.isfile(file1), f"Expected file missing: {file1}"
    assert os.path.isfile(file2), f"Expected file missing: {file2}"

    inode1 = os.stat(file1).st_ino
    inode2 = os.stat(file2).st_ino

    assert inode1 == inode2, (
        f"Deduplication failed: {file1} (inode {inode1}) and "
        f"{file2} (inode {inode2}) do not share the same inode."
    )

def test_backup_created():
    """Verify the incremental backup archive exists and is a valid gzip tar file."""
    backup_path = "/home/user/curated_backup.tar.gz"

    assert os.path.isfile(backup_path), f"Backup file missing: {backup_path}"

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            members = tar.getnames()
            assert len(members) > 0, "Backup archive is empty."
    except tarfile.ReadError:
        pytest.fail(f"Backup file {backup_path} is not a valid gzip-compressed tar archive.")