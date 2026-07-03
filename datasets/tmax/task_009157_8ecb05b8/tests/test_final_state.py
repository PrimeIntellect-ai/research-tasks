# test_final_state.py

import os
import stat
import pytest

def test_elf_checker_executable():
    elf_checker_path = "/home/user/elf_checker"
    assert os.path.exists(elf_checker_path), f"{elf_checker_path} does not exist."
    assert os.path.isfile(elf_checker_path), f"{elf_checker_path} is not a file."

    st = os.stat(elf_checker_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{elf_checker_path} is not executable."

def test_renamed_files():
    backup_dir = "/home/user/bin_backup"

    expected_renamed = [
        "serviceA_64.bin",
        "serviceB_64.bin",
        "legacy_worker_32.bin",
        "blob_data_UNKNOWN.bin"
    ]

    unexpected_original = [
        "serviceA.bin",
        "serviceB.bin",
        "legacy_worker.bin",
        "blob_data.bin"
    ]

    for filename in expected_renamed:
        filepath = os.path.join(backup_dir, filename)
        assert os.path.exists(filepath), f"Expected renamed file {filepath} does not exist."

    for filename in unexpected_original:
        filepath = os.path.join(backup_dir, filename)
        assert not os.path.exists(filepath), f"Original file {filepath} should have been renamed."

def test_links():
    archive_64_dir = "/home/user/bin_archive/64"
    archive_32_dir = "/home/user/bin_archive/32"
    backup_dir = "/home/user/bin_backup"

    # Check 64-bit hard links
    hard_links = ["serviceA_64.bin", "serviceB_64.bin"]
    for filename in hard_links:
        archive_path = os.path.join(archive_64_dir, filename)
        backup_path = os.path.join(backup_dir, filename)

        assert os.path.exists(archive_path), f"Hard link {archive_path} does not exist."
        assert not os.path.islink(archive_path), f"{archive_path} should be a hard link, not a symlink."

        st_archive = os.stat(archive_path)
        st_backup = os.stat(backup_path)
        assert st_archive.st_ino == st_backup.st_ino, f"{archive_path} and {backup_path} do not point to the same inode (not hard linked)."

    # Check 32-bit symlink
    symlink_filename = "legacy_worker_32.bin"
    archive_symlink_path = os.path.join(archive_32_dir, symlink_filename)
    backup_target_path = os.path.join(backup_dir, symlink_filename)

    assert os.path.exists(archive_symlink_path), f"Symlink {archive_symlink_path} does not exist."
    assert os.path.islink(archive_symlink_path), f"{archive_symlink_path} is not a symlink."

    target = os.readlink(archive_symlink_path)
    # Target could be absolute or relative, but it must resolve to the correct file
    resolved_target = os.path.abspath(os.path.join(archive_32_dir, target))
    assert resolved_target == backup_target_path, f"Symlink {archive_symlink_path} points to {resolved_target}, expected {backup_target_path}."

def test_readme_encoding():
    utf8_readme_path = "/home/user/bin_backup/readme_utf8.txt"
    assert os.path.exists(utf8_readme_path), f"{utf8_readme_path} does not exist."

    with open(utf8_readme_path, "rb") as f:
        content_bytes = f.read()

    try:
        content_str = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(f"File {utf8_readme_path} is not valid UTF-8.")

    expected_content = "Archiving requires attention to detail."
    assert content_str == expected_content, f"Content of {utf8_readme_path} does not match expected text."