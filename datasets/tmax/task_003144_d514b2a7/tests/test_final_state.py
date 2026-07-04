# test_final_state.py

import os
import pytest

RAW_DIR = "/home/user/raw_gcode"
DOCS_DIR = "/home/user/docs"
TREE_FILE = "/home/user/docs_tree.txt"

EXPECTED_MAPPING = [
    {
        "filename": "bracket.gcode",
        "printer": "Ender3",
        "material": "PLA"
    },
    {
        "filename": "gear.gcode",
        "printer": "PrusaMK3",
        "material": "PETG"
    },
    {
        "filename": "flex_joint.gcode",
        "printer": "Ender3",
        "material": "TPU"
    },
    {
        "filename": "test_cube.gcode",
        "printer": "Unknown",
        "material": "Unknown"
    }
]

def test_symlinks_by_printer():
    """Verify that symbolic links are correctly created in the by_printer directory."""
    for item in EXPECTED_MAPPING:
        symlink_path = os.path.join(
            DOCS_DIR, "by_printer", item["printer"], item["material"], item["filename"]
        )
        target_path = os.path.join(RAW_DIR, item["filename"])

        assert os.path.islink(symlink_path), f"Expected symbolic link missing or not a symlink: {symlink_path}"

        # Read the symlink target
        actual_target = os.readlink(symlink_path)
        # Handle both absolute and relative symlinks (though absolute is standard for this task)
        if not os.path.isabs(actual_target):
            actual_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), actual_target))

        assert actual_target == target_path, f"Symlink {symlink_path} points to {actual_target}, expected {target_path}"

def test_hardlinks_by_material():
    """Verify that hard links are correctly created in the by_material directory."""
    for item in EXPECTED_MAPPING:
        hardlink_path = os.path.join(
            DOCS_DIR, "by_material", item["material"], item["printer"], item["filename"]
        )
        original_path = os.path.join(RAW_DIR, item["filename"])

        assert os.path.exists(hardlink_path), f"Expected hard link missing: {hardlink_path}"
        assert not os.path.islink(hardlink_path), f"Expected a hard link, but found a symlink: {hardlink_path}"

        original_stat = os.stat(original_path)
        hardlink_stat = os.stat(hardlink_path)

        assert original_stat.st_ino == hardlink_stat.st_ino, (
            f"File {hardlink_path} is not a hard link to {original_path} "
            f"(inode {hardlink_stat.st_ino} != {original_stat.st_ino})"
        )

def test_tree_output_file():
    """Verify that the tree output file exists and contains expected content."""
    assert os.path.isfile(TREE_FILE), f"Tree output file is missing: {TREE_FILE}"

    with open(TREE_FILE, "r") as f:
        content = f.read()

    assert "by_printer" in content, "Tree output does not contain 'by_printer' directory."
    assert "by_material" in content, "Tree output does not contain 'by_material' directory."

    for item in EXPECTED_MAPPING:
        assert item["filename"] in content, f"Tree output is missing file: {item['filename']}"
        if item["printer"] != "Unknown":
            assert item["printer"] in content, f"Tree output is missing printer: {item['printer']}"
        if item["material"] != "Unknown":
            assert item["material"] in content, f"Tree output is missing material: {item['material']}"