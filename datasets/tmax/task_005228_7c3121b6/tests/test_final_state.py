import os
import stat
import tarfile
import pytest

def test_script_exists():
    script_path = "/home/user/config_archiver.py"
    assert os.path.isfile(script_path), f"Expected script at {script_path} does not exist."

def test_archive_exists_and_contents():
    archive_path = "/home/user/configs/archive/active_configs.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()

    expected_files = {"app_v05.cfg", "app_v10.cfg", "app_v15.cfg"}
    actual_files = set(members)

    assert actual_files == expected_files, f"Archive contents mismatch. Expected {expected_files}, got {actual_files}. Make sure files are stored at the root of the archive without full paths."

def test_symlink_latest_archive():
    symlink_path = "/home/user/configs/latest.tar.gz"
    target_path = "/home/user/configs/archive/active_configs.tar.gz"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    # Resolve the symlink to its absolute target
    resolved_target = os.path.realpath(symlink_path)
    expected_target = os.path.realpath(target_path)

    assert resolved_target == expected_target, f"Symlink {symlink_path} points to {resolved_target}, expected it to point to {expected_target}."

def test_hardlink_latest_valid_raw():
    hardlink_path = "/home/user/configs/latest_valid_raw.cfg"
    target_path = "/home/user/configs/raw/app_v15.cfg"

    assert os.path.isfile(hardlink_path), f"Hard link {hardlink_path} does not exist."
    assert os.path.isfile(target_path), f"Target file {target_path} does not exist."

    link_stat = os.stat(hardlink_path)
    target_stat = os.stat(target_path)

    assert link_stat.st_ino == target_stat.st_ino, f"{hardlink_path} is not a hard link to {target_path} (inodes do not match)."
    assert link_stat.st_dev == target_stat.st_dev, f"{hardlink_path} and {target_path} are on different devices."

def test_original_files_unmodified():
    # Ensure the original files were not deleted or modified
    expected_files = {
        "app_v10.cfg": 0o644,
        "app_v15.cfg": 0o644,
        "app_v05.cfg": 0o644,
        "app_v20_badperms.cfg": 0o600,
        "app_v30_badhead.cfg": 0o644,
    }

    for filename, expected_perms in expected_files.items():
        filepath = os.path.join("/home/user/configs/raw", filename)
        assert os.path.isfile(filepath), f"Original file {filepath} is missing. The script should not remove original files."

        file_stat = os.stat(filepath)
        actual_perms = stat.S_IMODE(file_stat.st_mode)
        assert actual_perms == expected_perms, f"Original file {filepath} permissions were modified."