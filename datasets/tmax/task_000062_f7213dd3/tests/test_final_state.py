# test_final_state.py

import os
import json
import tarfile
import pytest
import hashlib

def test_archive_exists():
    archive_path = "/home/user/repo/firmware_packaged.tar.gz"
    assert os.path.isfile(archive_path), f"Archive not found at {archive_path}"

def test_archive_contents_and_sizes():
    archive_path = "/home/user/repo/firmware_packaged.tar.gz"
    assert os.path.isfile(archive_path), "Archive not found"

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()

        # Check that there are exactly 3 files and no directories
        assert len(members) == 3, f"Expected 3 files in archive, found {len(members)}"

        names = sorted([m.name for m in members])
        expected_names = ["part_00", "part_01", "part_02"]
        # Allow optional ./ prefix
        names_cleaned = [n.replace("./", "") for n in names]
        assert names_cleaned == expected_names, f"Expected files {expected_names}, found {names_cleaned}"

        sizes = {}
        for m in members:
            sizes[m.name.replace("./", "")] = m.size

        assert sizes["part_00"] == 1000, f"part_00 size incorrect: {sizes['part_00']} != 1000"
        assert sizes["part_01"] == 1000, f"part_01 size incorrect: {sizes['part_01']} != 1000"
        assert sizes["part_02"] == 500, f"part_02 size incorrect: {sizes['part_02']} != 500"

def test_reassembled_content():
    archive_path = "/home/user/repo/firmware_packaged.tar.gz"
    firmware_path = "/home/user/firmware.bin"

    assert os.path.isfile(archive_path), "Archive not found"
    assert os.path.isfile(firmware_path), "Original firmware file not found"

    with open(firmware_path, "rb") as f:
        original_data = f.read()

    reassembled_data = bytearray()
    with tarfile.open(archive_path, "r:gz") as tar:
        # Find members accounting for optional ./ prefix
        part00 = next(m for m in tar.getmembers() if m.name.endswith("part_00"))
        part01 = next(m for m in tar.getmembers() if m.name.endswith("part_01"))
        part02 = next(m for m in tar.getmembers() if m.name.endswith("part_02"))

        reassembled_data.extend(tar.extractfile(part00).read())
        reassembled_data.extend(tar.extractfile(part01).read())
        reassembled_data.extend(tar.extractfile(part02).read())

    assert original_data == reassembled_data, "Reassembled chunks do not match the original firmware file"

def test_atomic_rename_in_code():
    code_path = "/home/user/curate.go"
    assert os.path.isfile(code_path), f"Go source file not found at {code_path}"

    with open(code_path, "r") as f:
        code = f.read()

    has_os_rename = "os.Rename" in code
    has_mv = "mv " in code
    assert has_os_rename or has_mv, "No atomic rename logic (os.Rename or mv) found in the Go source code"