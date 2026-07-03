# test_final_state.py

import os
import pytest

def test_c_program_exists():
    assert os.path.isfile("/home/user/doc_extractor.c"), "C source code /home/user/doc_extractor.c is missing."
    assert os.path.isfile("/home/user/doc_extractor"), "Compiled executable /home/user/doc_extractor is missing."
    assert os.access("/home/user/doc_extractor", os.X_OK), "Compiled executable is not marked as executable."

def test_extracted_files_content():
    expected_files = {
        "readme.txt": b"Welcome to the robotics documentation.\n" * 5,
        "calibrate.gcode": b"G28 X Y Z\nG1 X100 Y100 F3000\n" * 3,
        "firmware_boot.elf": b"\x7FELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00" + b"\x00" * 50
    }

    for filename, expected_data in expected_files.items():
        path = f"/home/user/extracted/{filename}"
        assert os.path.isfile(path), f"Extracted file is missing: {path}"
        with open(path, "rb") as f:
            data = f.read()
        assert data == expected_data, f"Content mismatch for {path}"

def test_symlinks_exist_and_correct():
    expected_symlinks = {
        "/home/user/docs/by_type/text/readme.txt": "/home/user/extracted/readme.txt",
        "/home/user/docs/by_type/gcode/calibrate.gcode": "/home/user/extracted/calibrate.gcode",
        "/home/user/docs/by_type/elf/firmware_boot.elf": "/home/user/extracted/firmware_boot.elf"
    }

    for symlink_path, target_path in expected_symlinks.items():
        assert os.path.islink(symlink_path), f"Expected symbolic link missing or not a symlink: {symlink_path}"
        actual_target = os.readlink(symlink_path)
        # Handle both absolute and relative symlinks that resolve to the correct file
        if not os.path.isabs(actual_target):
            actual_target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), actual_target))
        assert actual_target == target_path, f"Symlink {symlink_path} points to {actual_target}, expected {target_path}"

def test_manifest_content():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file missing: {manifest_path}"

    expected_lines = [
        "/home/user/docs/by_type/elf/firmware_boot.elf",
        "/home/user/docs/by_type/gcode/calibrate.gcode",
        "/home/user/docs/by_type/text/readme.txt"
    ]

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_lines, "Manifest contents do not match expected sorted list of absolute paths."