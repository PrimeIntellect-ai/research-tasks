# test_final_state.py

import os
import hashlib
import pytest

ARCHIVE_DIR = "/home/user/archive"
MANIFEST_PATH = os.path.join(ARCHIVE_DIR, "manifest.txt")

def get_sha256(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def test_manifest_exists():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file not found at {MANIFEST_PATH}"
    assert os.path.isfile(MANIFEST_PATH), f"{MANIFEST_PATH} is not a file"

def test_large_file_chunked():
    orig_large = "/home/user/monitored_data/app_configs/large_db.sqlite"
    for part in ["aa", "ab", "ac"]:
        chunk_name = f"large_db.sqlite.part_{part}"
        chunk_path = os.path.join(ARCHIVE_DIR, chunk_name)
        assert os.path.exists(chunk_path), f"Expected chunk {chunk_name} missing in archive for file > 50KB"
        assert os.path.isfile(chunk_path), f"{chunk_path} is not a file"

def test_small_files_copied():
    small_config = os.path.join(ARCHIVE_DIR, "small_config.txt")
    settings_json = os.path.join(ARCHIVE_DIR, "settings.json")

    assert os.path.exists(small_config), f"small_config.txt missing in archive"
    assert os.path.exists(settings_json), f"settings.json missing in archive"

def test_manifest_contents():
    assert os.path.exists(MANIFEST_PATH), "Manifest file must exist to check contents"

    expected_lines = []

    # large_db.sqlite chunks
    orig_large = "/home/user/monitored_data/app_configs/large_db.sqlite"
    for part in ["aa", "ab", "ac"]:
        chunk_name = f"large_db.sqlite.part_{part}"
        chunk_path = os.path.join(ARCHIVE_DIR, chunk_name)
        if os.path.exists(chunk_path):
            h = get_sha256(chunk_path)
            expected_lines.append(f"{orig_large} | {chunk_name} | {h}")

    # small_config.txt
    orig_small = "/home/user/monitored_data/app_configs/small_config.txt"
    small_path = os.path.join(ARCHIVE_DIR, "small_config.txt")
    if os.path.exists(small_path):
        h = get_sha256(small_path)
        expected_lines.append(f"{orig_small} | small_config.txt | {h}")

    # settings.json
    orig_json = "/home/user/monitored_data/app_configs/nested/settings.json"
    json_path = os.path.join(ARCHIVE_DIR, "settings.json")
    if os.path.exists(json_path):
        h = get_sha256(json_path)
        expected_lines.append(f"{orig_json} | settings.json | {h}")

    expected_lines.sort()

    with open(MANIFEST_PATH, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, "Manifest contents do not match expected sorted output with correct checksums"