# test_final_state.py

import os
import tarfile
import pytest

def test_curated_repo_files_exist():
    expected_files = [
        "stable_app_v1.bin",
        "stable_Network_Tool_v2.bin",
        "stable_script_file.bin",
        "stable_patch.bin"
    ]

    curated_dir = "/home/user/curated_repo"
    assert os.path.isdir(curated_dir), f"Directory {curated_dir} does not exist."

    actual_files = set(os.listdir(curated_dir))

    for f in expected_files:
        assert f in actual_files, f"Expected file {f} is missing from {curated_dir}."

    # Check that non-matching files were not copied
    unexpected_files = [
        "stable_small_app.bin",
        "stable_library.bin"
    ]
    for f in unexpected_files:
        assert f not in actual_files, f"File {f} should not be in {curated_dir}."

def test_backup_files_exist():
    backup_dir = "/home/user/backup"
    expected_files = ["full.tar", "inc.tar", "repo.snar"]

    assert os.path.isdir(backup_dir), f"Directory {backup_dir} does not exist."

    for f in expected_files:
        path = os.path.join(backup_dir, f)
        assert os.path.isfile(path), f"Backup file {path} is missing."

def test_inc_tar_contents():
    inc_tar_path = "/home/user/backup/inc.tar"
    assert tarfile.is_tarfile(inc_tar_path), f"{inc_tar_path} is not a valid tar file."

    with tarfile.open(inc_tar_path, "r") as tar:
        members = [m.name for m in tar.getmembers()]

        # stable_patch.bin must be in inc.tar
        patch_found = any(m.endswith("stable_patch.bin") for m in members)
        assert patch_found, f"stable_patch.bin was not found in {inc_tar_path}."

        # Check that the payload for previously backed up files is not included
        # GNU tar incremental backups might include directory entries, but file entries for 
        # unchanged files should not be present (or have size 0 if just metadata).
        # We will check for file entries that are not directories.
        for m in tar.getmembers():
            if m.isfile() and not m.name.endswith("stable_patch.bin"):
                # If it's a file but not stable_patch.bin, it shouldn't be here
                # Note: depending on tar version, it might not include unchanged files at all.
                # Just fail if we see the old files as regular files with size > 0
                if any(old_file in m.name for old_file in ["stable_app_v1.bin", "stable_Network_Tool_v2.bin", "stable_script_file.bin"]):
                    assert m.size == 0, f"Unchanged file {m.name} was included with data in incremental backup."