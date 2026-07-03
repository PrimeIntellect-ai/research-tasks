# test_final_state.py
import os
import json
import hashlib
import pytest

RAW_DIR = "/home/user/backups/raw"
PROCESSED_DIR = "/home/user/backups/processed"
MANIFEST_PATH = "/home/user/backups/manifest.json"

EXPECTED_ORIGINAL_FILES = {
    "export_A_final.txt",
    "db_dump_random.txt",
    "cache-log-11.txt"
}

EXPECTED_PROCESSED_FILES = {
    "web01_20231024.csv",
    "db_main_20231025.csv",
    "redis_01_20231026.csv"
}

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def test_raw_directory_empty():
    assert os.path.exists(RAW_DIR), f"Directory {RAW_DIR} does not exist."
    files = os.listdir(RAW_DIR)
    assert len(files) == 0, f"Raw directory {RAW_DIR} is not empty. Contains: {files}"

def test_processed_files_exist_and_lowercase():
    assert os.path.exists(PROCESSED_DIR), f"Directory {PROCESSED_DIR} does not exist."

    actual_files = set(os.listdir(PROCESSED_DIR))
    for expected_file in EXPECTED_PROCESSED_FILES:
        assert expected_file in actual_files, f"Expected processed file '{expected_file}' not found in {PROCESSED_DIR}."

        filepath = os.path.join(PROCESSED_DIR, expected_file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        assert content == content.lower(), f"File '{expected_file}' is not entirely lowercase."

def test_manifest_structure_and_checksums():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {MANIFEST_PATH} is not valid JSON.")

    assert "archives" in manifest, "Manifest JSON is missing the 'archives' key."
    archives = manifest["archives"]
    assert isinstance(archives, list), "'archives' must be a list."
    assert len(archives) == len(EXPECTED_ORIGINAL_FILES), f"Expected {len(EXPECTED_ORIGINAL_FILES)} entries in 'archives', found {len(archives)}."

    manifest_originals = set()
    manifest_processed = set()

    for entry in archives:
        assert "original" in entry, "An entry in 'archives' is missing the 'original' key."
        assert "processed" in entry, "An entry in 'archives' is missing the 'processed' key."
        assert "checksum" in entry, "An entry in 'archives' is missing the 'checksum' key."

        orig = entry["original"]
        proc = entry["processed"]
        chk = entry["checksum"]

        manifest_originals.add(orig)
        manifest_processed.add(proc)

        proc_path = os.path.join(PROCESSED_DIR, proc)
        assert os.path.exists(proc_path), f"Processed file '{proc}' referenced in manifest does not exist in {PROCESSED_DIR}."

        actual_checksum = get_sha256(proc_path)
        assert chk == actual_checksum, f"Checksum mismatch for '{proc}'. Expected (from manifest): {chk}, Actual: {actual_checksum}"

    assert manifest_originals == EXPECTED_ORIGINAL_FILES, f"Manifest 'original' files do not match expected. Expected: {EXPECTED_ORIGINAL_FILES}, Found: {manifest_originals}"
    assert manifest_processed == EXPECTED_PROCESSED_FILES, f"Manifest 'processed' files do not match expected. Expected: {EXPECTED_PROCESSED_FILES}, Found: {manifest_processed}"