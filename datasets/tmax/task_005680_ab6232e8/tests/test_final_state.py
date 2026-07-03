# test_final_state.py

import os
import csv
import json
import base64
import pytest

CONFIG_PATH = "/home/user/backup_config.json"
MANIFEST_PATH = "/home/user/backup_manifest.csv"
SYMLINK_LOG_PATH = "/home/user/symlink_loops.log"
SOURCE_DIR = "/home/user/source_data"
DEST_DIR = "/home/user/backup_dest"

@pytest.fixture(scope="module")
def config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def test_symlink_loops_logged():
    assert os.path.exists(SYMLINK_LOG_PATH), f"Symlink log file missing at {SYMLINK_LOG_PATH}"
    with open(SYMLINK_LOG_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_loops = {
        "/home/user/source_data/level1/level2/loop_link",
        "/home/user/source_data/level1/valid_link/loop_link"
    }

    assert len(lines) > 0, "Symlink log is empty, expected to find loop links."
    for line in lines:
        assert line in expected_loops, f"Unexpected symlink loop logged: {line}"

def test_manifest_exists_and_format():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"

    with open(MANIFEST_PATH, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["original_path", "base64_length"], "Manifest header is incorrect."

        rows = list(reader)
        assert len(rows) >= 3, "Manifest should contain at least the 3 original files."

        for row in rows:
            assert len(row) == 2, f"Invalid manifest row: {row}"
            path, length = row
            assert path.startswith(SOURCE_DIR), f"Path in manifest does not start with source_dir: {path}"
            assert length.isdigit(), f"Length in manifest is not a digit: {length}"

def test_backed_up_files(config):
    encodings = config["encodings"]
    compression_key = config["compression_key"]

    assert os.path.exists(MANIFEST_PATH), "Manifest missing."

    with open(MANIFEST_PATH, "r") as f:
        reader = csv.reader(f)
        next(reader) # skip header
        manifest_entries = list(reader)

    for original_path, b64_length in manifest_entries:
        # Determine relative path
        rel_path = os.path.relpath(original_path, SOURCE_DIR)
        dest_path = os.path.join(DEST_DIR, rel_path) + ".bak"

        assert os.path.exists(dest_path), f"Backup file missing: {dest_path}"

        # Read backup file
        with open(dest_path, "r") as f:
            b64_content = f.read().strip()

        assert len(b64_content) == int(b64_length), f"Manifest length {b64_length} does not match actual length {len(b64_content)} for {dest_path}"

        # Decode and un-XOR
        try:
            xor_bytes = base64.b64decode(b64_content)
        except Exception as e:
            pytest.fail(f"Failed to decode base64 for {dest_path}: {e}")

        unxored_bytes = bytes(b ^ compression_key for b in xor_bytes)

        try:
            restored_text = unxored_bytes.decode("utf-8")
        except Exception as e:
            pytest.fail(f"Failed to decode UTF-8 after un-XOR for {dest_path}: {e}")

        # Read original file
        _, ext = os.path.splitext(original_path)
        encoding = encodings.get(ext, "utf-8")

        with open(original_path, "r", encoding=encoding) as f:
            original_text = f.read()

        assert restored_text == original_text, f"Restored content does not match original for {original_path}"