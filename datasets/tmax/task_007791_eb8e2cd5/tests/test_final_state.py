# test_final_state.py

import os
import pytest

BACKUP_DEST = "/home/user/backup_dest"
BACKUP_LOG = "/home/user/backup_log.txt"
DATA_SOURCE = "/home/user/data_source"
LAST_BACKUP_TS = "/home/user/last_backup.ts"

def test_backup_dest_exists():
    assert os.path.isdir(BACKUP_DEST), f"Destination directory {BACKUP_DEST} was not created or is not a directory."

def test_old_files_not_copied():
    old1 = os.path.join(BACKUP_DEST, "folderA", "old1.txt")
    old2 = os.path.join(BACKUP_DEST, "folderB", "old2.txt")
    old1_hlink = os.path.join(BACKUP_DEST, "folderB", "old1_hlink.txt")

    assert not os.path.exists(old1), "old1.txt should not have been copied (older than last_backup.ts)."
    assert not os.path.exists(old2), "old2.txt should not have been copied (older than last_backup.ts)."
    assert not os.path.exists(old1_hlink), "old1_hlink.txt should not have been copied (older than last_backup.ts)."

def test_new_files_and_hardlinks_copied():
    new1 = os.path.join(BACKUP_DEST, "folderA", "new1.txt")
    new2 = os.path.join(BACKUP_DEST, "folderA", "new2.txt")
    new1_hlink = os.path.join(BACKUP_DEST, "folderB", "new1_hlink.txt")
    new2_hlink = os.path.join(BACKUP_DEST, "folderA", "new2_hlink.txt")

    assert os.path.isfile(new1) and not os.path.islink(new1), "new1.txt was not copied correctly."
    assert os.path.isfile(new2) and not os.path.islink(new2), "new2.txt was not copied correctly."
    assert os.path.isfile(new1_hlink) and not os.path.islink(new1_hlink), "new1_hlink.txt was not copied correctly."
    assert os.path.isfile(new2_hlink) and not os.path.islink(new2_hlink), "new2_hlink.txt was not copied correctly."

    # Check hardlink preservation
    assert os.stat(new1).st_ino == os.stat(new1_hlink).st_ino, "new1.txt and new1_hlink.txt do not share the same inode in destination."
    assert os.stat(new2).st_ino == os.stat(new2_hlink).st_ino, "new2.txt and new2_hlink.txt do not share the same inode in destination."

def test_symlinks_copied_correctly():
    sym_old = os.path.join(BACKUP_DEST, "folderB", "sym_to_old.txt")
    sym_new = os.path.join(BACKUP_DEST, "folderB", "sym_to_new.txt")

    assert os.path.islink(sym_old), "sym_to_old.txt was not copied as a symlink."
    assert os.path.islink(sym_new), "sym_to_new.txt was not copied as a symlink."

    assert os.readlink(sym_old) == "../folderA/old1.txt", "sym_to_old.txt target was not preserved."
    assert os.readlink(sym_new) == "../folderA/new1.txt", "sym_to_new.txt target was not preserved."

def test_backup_log_exists_and_format():
    assert os.path.isfile(BACKUP_LOG), f"Log file {BACKUP_LOG} is missing."

    with open(BACKUP_LOG, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Expected items
    expected_items = {
        "folderA/new1.txt",
        "folderA/new2.txt",
        "folderA/new2_hlink.txt",
        "folderB/new1_hlink.txt",
        "folderB/sym_to_new.txt",
        "folderB/sym_to_old.txt"
    }

    parsed_items = []
    log_dict = {}

    for line in lines:
        parts = line.split(" ", 1)
        assert len(parts) == 2, f"Log line format invalid: {line}"
        item_type, path = parts
        assert item_type in ("[FILE]", "[HLINK]", "[SLINK]"), f"Invalid type marker {item_type} in log."
        parsed_items.append(path)
        log_dict[path] = item_type

    assert set(parsed_items) == expected_items, f"Log items do not match expected backed up files. Expected: {expected_items}, Got: {set(parsed_items)}"

    # Check sorting
    assert parsed_items == sorted(parsed_items), "Log file is not sorted alphabetically by relative path."

    # Check symlinks
    assert log_dict["folderB/sym_to_new.txt"] == "[SLINK]", "sym_to_new.txt should be marked as [SLINK]"
    assert log_dict["folderB/sym_to_old.txt"] == "[SLINK]", "sym_to_old.txt should be marked as [SLINK]"

    # Check hardlinks logic
    new1_group = ["folderA/new1.txt", "folderB/new1_hlink.txt"]
    new2_group = ["folderA/new2.txt", "folderA/new2_hlink.txt"]

    for group in (new1_group, new2_group):
        types = [log_dict[path] for path in group]
        file_count = types.count("[FILE]")
        hlink_count = types.count("[HLINK]")
        assert file_count == 1, f"Expected exactly one [FILE] for shared inode group {group}, got {file_count}."
        assert hlink_count == len(group) - 1, f"Expected {len(group) - 1} [HLINK] for shared inode group {group}, got {hlink_count}."