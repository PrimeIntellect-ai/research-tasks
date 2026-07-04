# test_final_state.py

import os
import json
import pytest

ASSETS_DIR = "/home/user/project_assets"
ORGANIZED_DIR = "/home/user/organized"
BIN_DIR = os.path.join(ORGANIZED_DIR, "bin")
TXT_DIR = os.path.join(ORGANIZED_DIR, "txt")
MANIFEST_PATH = os.path.join(ORGANIZED_DIR, "manifest.json")

EXPECTED_TEXT = ["config.json", "readme.md", "script.py"]
EXPECTED_BIN = ["logo.gif", "executable.bin", "mixed.dat"]

def test_directories_exist():
    assert os.path.isdir(BIN_DIR), f"{BIN_DIR} directory is missing"
    assert os.path.isdir(TXT_DIR), f"{TXT_DIR} directory is missing"

def test_text_files_symlinked():
    for filename in EXPECTED_TEXT:
        orig_path = os.path.join(ASSETS_DIR, filename)
        link_path = os.path.join(TXT_DIR, filename)

        assert os.path.exists(link_path), f"Link for {filename} is missing in {TXT_DIR}"
        assert os.path.islink(link_path), f"{link_path} is not a symbolic link"

        target = os.readlink(link_path)
        assert target == orig_path, f"Symlink {link_path} does not point to {orig_path} (got {target})"

def test_binary_files_hardlinked():
    for filename in EXPECTED_BIN:
        orig_path = os.path.join(ASSETS_DIR, filename)
        link_path = os.path.join(BIN_DIR, filename)

        assert os.path.exists(link_path), f"Link for {filename} is missing in {BIN_DIR}"
        assert not os.path.islink(link_path), f"{link_path} should be a hard link, not a symbolic link"

        orig_stat = os.stat(orig_path)
        link_stat = os.stat(link_path)
        assert orig_stat.st_ino == link_stat.st_ino, f"{link_path} is not hardlinked to {orig_path} (inodes differ)"

def test_manifest_json():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"

    with open(MANIFEST_PATH, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{MANIFEST_PATH} is not valid JSON")

    for filename in EXPECTED_TEXT:
        assert filename in manifest, f"{filename} missing from manifest"
        assert manifest[filename].get("type") == "text", f"Wrong type for {filename} in manifest"
        expected_link = os.path.join(TXT_DIR, filename)
        assert manifest[filename].get("link_path") == expected_link, f"Wrong link_path for {filename} in manifest"

    for filename in EXPECTED_BIN:
        assert filename in manifest, f"{filename} missing from manifest"
        assert manifest[filename].get("type") == "binary", f"Wrong type for {filename} in manifest"
        expected_link = os.path.join(BIN_DIR, filename)
        assert manifest[filename].get("link_path") == expected_link, f"Wrong link_path for {filename} in manifest"