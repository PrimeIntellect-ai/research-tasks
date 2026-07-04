# test_final_state.py

import os
import zlib
import base64
import pytest

ARCHIVE_DIR = "/home/user/archive"
MANIFEST_PATH = os.path.join(ARCHIVE_DIR, "manifest.txt")
PROCESS_SCRIPT = "/home/user/process.sh"

EXPECTED_FILES = {
    "intro.md": {
        "original": "/home/user/drafts/networking/intro.md",
        "archived": "intro.z64"
    },
    "endpoints.md": {
        "original": "/home/user/drafts/api/v1/endpoints.md",
        "archived": "endpoints.z64"
    },
    "summary.md": {
        "original": "/home/user/drafts/summary.md",
        "archived": "summary.z64"
    }
}

def test_process_script_exists_and_uses_flock():
    assert os.path.isfile(PROCESS_SCRIPT), f"Processing script {PROCESS_SCRIPT} is missing."
    with open(PROCESS_SCRIPT, 'r') as f:
        content = f.read()
    assert "flock" in content, f"The script {PROCESS_SCRIPT} does not seem to use 'flock' as required."

def test_archive_directory_exists():
    assert os.path.isdir(ARCHIVE_DIR), f"Destination directory {ARCHIVE_DIR} does not exist."

def test_archived_files_exist_and_content_matches():
    for md_file, paths in EXPECTED_FILES.items():
        archived_path = os.path.join(ARCHIVE_DIR, paths["archived"])
        original_path = paths["original"]

        assert os.path.isfile(archived_path), f"Archived file {archived_path} is missing."
        assert os.path.isfile(original_path), f"Original file {original_path} is missing."

        with open(original_path, 'r') as f:
            original_content = f.read()

        with open(archived_path, 'r') as f:
            encoded_content = f.read()

        try:
            compressed_data = base64.b64decode(encoded_content)
            decompressed_content = zlib.decompress(compressed_data).decode('utf-8')
        except Exception as e:
            pytest.fail(f"Failed to decode/decompress {archived_path}: {e}")

        assert decompressed_content == original_content, f"Decompressed content of {archived_path} does not match original {original_path}."

def test_manifest_file_correct():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} is missing."

    with open(MANIFEST_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Manifest file should contain exactly 3 lines, found {len(lines)}."

    expected_entries = set()
    for paths in EXPECTED_FILES.values():
        expected_entries.add(f"{paths['archived']}:{paths['original']}")

    actual_entries = set(lines)

    assert actual_entries == expected_entries, f"Manifest entries do not match expected format and content. Expected: {expected_entries}, Found: {actual_entries}"