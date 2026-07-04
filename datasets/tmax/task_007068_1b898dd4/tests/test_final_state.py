# test_final_state.py

import os
import hashlib
import pytest

PROJECT_BLOBS_DIR = "/home/user/project_blobs"
ORGANIZED_ZIPS_DIR = "/home/user/organized_zips"
MANIFEST_FILE = "/home/user/zip_manifest.txt"

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_expected_zips():
    expected_zips = {}
    for root, _, files in os.walk(PROJECT_BLOBS_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "rb") as f:
                    header = f.read(4)
                if header == b'\x50\x4b\x03\x04':
                    checksum = get_sha256(filepath)
                    stat = os.stat(filepath)
                    size = stat.st_size
                    inode = stat.st_ino
                    if checksum not in expected_zips:
                        expected_zips[checksum] = {
                            "size": size,
                            "inodes": set()
                        }
                    expected_zips[checksum]["inodes"].add(inode)
            except Exception:
                pass
    return expected_zips

def test_organized_zips_directory_exists():
    assert os.path.isdir(ORGANIZED_ZIPS_DIR), f"The directory {ORGANIZED_ZIPS_DIR} does not exist."

def test_organized_zips_contents_and_hard_links():
    expected_zips = get_expected_zips()

    assert len(expected_zips) > 0, "No valid ZIP files found in the source directory."

    files_in_organized = os.listdir(ORGANIZED_ZIPS_DIR)
    assert len(files_in_organized) == len(expected_zips), \
        f"Expected {len(expected_zips)} files in {ORGANIZED_ZIPS_DIR}, but found {len(files_in_organized)}."

    for filename in files_in_organized:
        assert filename.endswith(".zip"), f"File {filename} in {ORGANIZED_ZIPS_DIR} does not end with .zip"
        checksum = filename[:-4]
        assert checksum in expected_zips, f"File {filename} has an unexpected checksum name."

        filepath = os.path.join(ORGANIZED_ZIPS_DIR, filename)
        stat = os.stat(filepath)

        # Verify it's a hard link to one of the original files
        assert stat.st_ino in expected_zips[checksum]["inodes"], \
            f"File {filename} is not a hard link to the original file (inode mismatch)."

def test_manifest_file_correctness():
    assert os.path.isfile(MANIFEST_FILE), f"The manifest file {MANIFEST_FILE} does not exist."

    expected_zips = get_expected_zips()
    expected_lines = []
    for checksum, info in expected_zips.items():
        expected_lines.append(f"{checksum} {info['size']}")
    expected_lines.sort()

    with open(MANIFEST_FILE, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, \
        f"The contents of {MANIFEST_FILE} do not match the expected output. " \
        f"Expected: {expected_lines}, Actual: {actual_lines}"