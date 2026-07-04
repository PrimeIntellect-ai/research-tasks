# test_final_state.py
import os
import glob
import pytest

def test_directories_exist():
    """Check if the required directories exist."""
    assert os.path.isdir("/home/user/extracted_errors"), "Directory /home/user/extracted_errors was not created."
    assert os.path.isdir("/home/user/important_errors"), "Directory /home/user/important_errors was not created."

def test_extracted_and_renamed_files():
    """Check if the specific error files were extracted and renamed correctly."""
    expected_bases = ["db_timeout", "disk_full", "auth_fail"]

    for base in expected_bases:
        extracted_file = f"/home/user/extracted_errors/{base}.err"
        assert os.path.isfile(extracted_file), f"Missing extracted file: {extracted_file}"

def test_hard_links_created_and_valid():
    """Check if hard links were created correctly and share the same inode."""
    expected_bases = ["db_timeout", "disk_full", "auth_fail"]

    for base in expected_bases:
        extracted_file = f"/home/user/extracted_errors/{base}.err"
        hard_link_file = f"/home/user/important_errors/CRITICAL_{base}.err"

        assert os.path.isfile(hard_link_file), f"Missing hard link: {hard_link_file}"

        stat_extracted = os.stat(extracted_file)
        stat_link = os.stat(hard_link_file)

        assert stat_extracted.st_ino == stat_link.st_ino, f"Files do not share the same inode: {extracted_file} and {hard_link_file}"

def test_no_info_files_extracted():
    """Check that no .info files were incorrectly extracted."""
    info_files = glob.glob("/home/user/extracted_errors/*.info*")
    assert len(info_files) == 0, f"Info logs were incorrectly extracted: {info_files}"

def test_no_recombined_tarball():
    """Check that no recombined tarball was written to disk."""
    backup_tarballs = glob.glob("/home/user/backup_data/*.tar.gz")
    user_tarballs = glob.glob("/home/user/*.tar.gz")

    assert len(backup_tarballs) == 0, f"Recombined tarball written to /home/user/backup_data/: {backup_tarballs}"
    assert len(user_tarballs) == 0, f"Recombined tarball written to /home/user/: {user_tarballs}"