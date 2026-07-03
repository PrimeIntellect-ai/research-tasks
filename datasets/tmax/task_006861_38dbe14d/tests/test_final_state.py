# test_final_state.py

import os
import json
import pytest

DUMP_DIR = "/home/user/project_dump"
ORG_DIR = "/home/user/organized_assets"
INDEX_FILE = os.path.join(ORG_DIR, "index.json")

def test_hardlinks_created():
    """Check that duplicate files were replaced with hardlinks to the base file."""
    pairs = [
        ("asset_01.bin", "asset_02.bin"),
        ("data_01.dat", "data_03.dat"),
        ("sys_01.log", "sys_03.log")
    ]

    for base, dup in pairs:
        base_path = os.path.join(DUMP_DIR, base)
        dup_path = os.path.join(DUMP_DIR, dup)

        assert os.path.exists(base_path), f"Base file missing: {base_path}"
        assert os.path.exists(dup_path), f"Duplicate file missing: {dup_path}"

        base_stat = os.stat(base_path)
        dup_stat = os.stat(dup_path)

        assert base_stat.st_ino == dup_stat.st_ino, (
            f"Files {base} and {dup} do not share the same inode. "
            "They should be hardlinked."
        )

def test_symlink_organization():
    """Check that symlinks are correctly organized into subdirectories."""
    expected_symlinks = [
        ("image", "asset_01.bin"),
        ("image", "asset_03.bin"),
        ("custom", "data_01.dat"),
        ("custom", "data_02.dat"),
        ("log", "sys_01.log"),
        ("log", "sys_02.log")
    ]

    for category, filename in expected_symlinks:
        symlink_path = os.path.join(ORG_DIR, category, filename)
        target_path = os.path.join(DUMP_DIR, filename)

        assert os.path.islink(symlink_path), f"Expected symlink at {symlink_path}"

        actual_target = os.readlink(symlink_path)
        # Handle both absolute and relative symlinks that resolve correctly
        resolved_target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), actual_target))

        assert resolved_target == target_path, (
            f"Symlink {symlink_path} points to {actual_target}, "
            f"but should point to {target_path}"
        )

def test_index_json_content():
    """Check that the index.json file contains the correct metadata and is sorted."""
    assert os.path.exists(INDEX_FILE), f"Index file missing: {INDEX_FILE}"

    with open(INDEX_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {INDEX_FILE} is not valid JSON.")

    expected_data = [
        {"file": "asset_01.bin", "type": "image", "hardlinks": 2},
        {"file": "asset_03.bin", "type": "image", "hardlinks": 1},
        {"file": "data_01.dat", "type": "custom", "hardlinks": 2},
        {"file": "data_02.dat", "type": "custom", "hardlinks": 1},
        {"file": "sys_01.log", "type": "log", "hardlinks": 2},
        {"file": "sys_02.log", "type": "log", "hardlinks": 1}
    ]

    assert isinstance(data, list), "JSON root must be a list (array)."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in JSON, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual == expected, (
            f"Mismatch at index {i} in JSON.\n"
            f"Expected: {expected}\n"
            f"Got: {actual}"
        )