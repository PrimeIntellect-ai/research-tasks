# test_final_state.py

import os
import json
import pytest

BACKUP_DIR = "/home/user/incremental_backup"
MANIFEST_PATH = os.path.join(BACKUP_DIR, "manifest.json")

def test_manifest_exists_and_content():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file does not exist at {MANIFEST_PATH}"

    with open(MANIFEST_PATH, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest file is not valid JSON")

    assert isinstance(manifest, list), "Manifest must be a JSON array"

    expected_manifest = ["config/settings.xml", "logs/app.json", "logs/data.csv"]

    assert manifest == expected_manifest, (
        f"Manifest content mismatch. Expected {expected_manifest}, but got {manifest}. "
        "Ensure paths are relative, filtered correctly, and sorted alphabetically."
    )

def test_copied_files_match_manifest():
    expected_files = ["config/settings.xml", "logs/app.json", "logs/data.csv"]

    copied_files = []
    if os.path.exists(BACKUP_DIR):
        for root, _, files in os.walk(BACKUP_DIR):
            for file in files:
                if file not in ("manifest.json", "manifest.tmp"):
                    rel_path = os.path.relpath(os.path.join(root, file), BACKUP_DIR)
                    copied_files.append(rel_path)

    assert sorted(copied_files) == sorted(expected_files), (
        f"Copied files mismatch. Expected {sorted(expected_files)}, but got {sorted(copied_files)}. "
        "Ensure files are filtered by extension, excluded directories, and mtime strictly after last_run."
    )

    # Verify each expected file actually exists and is a file
    for f in expected_files:
        full_path = os.path.join(BACKUP_DIR, f)
        assert os.path.isfile(full_path), f"Expected backed up file {full_path} is missing or not a file."