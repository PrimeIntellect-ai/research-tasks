# test_final_state.py

import os
import pytest

def test_deduplication_hard_links():
    # Group A: 3 files
    file1 = "/home/user/storage_dump/docs/file1.txt"
    file2 = "/home/user/storage_dump/docs/nested/file2.txt"
    file3 = "/home/user/storage_dump/docs/nested/file3.txt"

    # Group B: 1 file
    file4 = "/home/user/storage_dump/docs/file4.txt"

    # Group C: 2 files
    file5 = "/home/user/storage_dump/file5.txt"
    file6 = "/home/user/storage_dump/logs/file6.txt"

    # Check existence
    for f in [file1, file2, file3, file4, file5, file6]:
        assert os.path.isfile(f), f"File {f} is missing."

    stat1 = os.stat(file1)
    stat2 = os.stat(file2)
    stat3 = os.stat(file3)

    assert stat1.st_nlink == 3, f"{file1} should have 3 hard links, got {stat1.st_nlink}."
    assert stat1.st_ino == stat2.st_ino == stat3.st_ino, "Files 1, 2, and 3 do not share the same inode."

    stat5 = os.stat(file5)
    stat6 = os.stat(file6)

    assert stat5.st_nlink == 2, f"{file5} should have 2 hard links, got {stat5.st_nlink}."
    assert stat5.st_ino == stat6.st_ino, "Files 5 and 6 do not share the same inode."

    stat4 = os.stat(file4)
    assert stat4.st_nlink == 1, f"{file4} should have 1 hard link, got {stat4.st_nlink}."

def test_archive_reassembly_and_symlink():
    extracted_file = "/home/user/extracted_backup/backup_src/secret.txt"
    assert os.path.isfile(extracted_file), f"Extracted file {extracted_file} does not exist."

    with open(extracted_file, 'r') as f:
        content = f.read().strip()
    assert content == "Secret Backup Data", f"Content of {extracted_file} is incorrect."

    symlink_path = "/home/user/latest_backup"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    # The target could be /home/user/extracted_backup or /home/user/extracted_backup/
    assert target.rstrip('/') == "/home/user/extracted_backup", f"Symlink points to incorrect target: {target}"

def test_log_extraction():
    output_file = "/home/user/critical_errors.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        content = f.read()

    block1 = "[CRITICAL_START]\nError ID: 101\nModule: Auth\nReason: Timeout\n[CRITICAL_END]"
    block2 = "[CRITICAL_START]\nError ID: 102\nModule: DB\nReason: OOM\n[CRITICAL_END]"

    assert block1 in content, "Block 1 (Error ID: 101) is missing from the output file."
    assert block2 in content, "Block 2 (Error ID: 102) is missing from the output file."

    # Verify no other unexpected content is present (allow for newlines between/after blocks)
    clean_content = content.replace(block1, "").replace(block2, "").strip()
    assert clean_content == "", "Output file contains extra unexpected content outside of the critical blocks."