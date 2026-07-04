# test_final_state.py

import os
import pytest

def test_hard_links_for_long_prints():
    long_prints = [
        ("part_A.gcode", "/home/user/gcode_files/part_A.gcode"),
        ("part_D.gcode", "/home/user/gcode_files/part_D.gcode"),
    ]

    long_prints_dir = "/home/user/archive/long_prints"

    for filename, original_path in long_prints:
        archived_path = os.path.join(long_prints_dir, filename)

        assert os.path.exists(archived_path), f"Expected hard link {archived_path} does not exist."
        assert not os.path.islink(archived_path), f"Expected {archived_path} to be a hard link, but it is a symlink."

        stat_original = os.stat(original_path)
        stat_archived = os.stat(archived_path)

        assert stat_original.st_ino == stat_archived.st_ino, f"File {archived_path} is not a hard link to {original_path} (inodes differ)."
        assert stat_original.st_dev == stat_archived.st_dev, f"File {archived_path} is not on the same device as {original_path}."

def test_symlinks_for_short_prints():
    short_prints = [
        ("part_B.gcode", "/home/user/gcode_files/part_B.gcode"),
    ]

    short_prints_dir = "/home/user/archive/short_prints"

    for filename, original_path in short_prints:
        archived_path = os.path.join(short_prints_dir, filename)

        assert os.path.islink(archived_path), f"Expected {archived_path} to be a symlink."

        target = os.readlink(archived_path)
        assert target == original_path, f"Symlink {archived_path} points to {target}, expected {original_path}."

def test_ignored_files():
    ignored_files = ["part_C.gcode"]
    long_prints_dir = "/home/user/archive/long_prints"
    short_prints_dir = "/home/user/archive/short_prints"

    for filename in ignored_files:
        long_path = os.path.join(long_prints_dir, filename)
        short_path = os.path.join(short_prints_dir, filename)

        assert not os.path.exists(long_path) and not os.path.islink(long_path), f"File {filename} should be ignored, but found in {long_prints_dir}."
        assert not os.path.exists(short_path) and not os.path.islink(short_path), f"File {filename} should be ignored, but found in {short_prints_dir}."