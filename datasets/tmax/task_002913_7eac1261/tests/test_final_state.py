# test_final_state.py
import os
import json
import zipfile
import pytest

def test_go_file_exists():
    path = "/home/user/organize.go"
    assert os.path.isfile(path), f"Missing Go source file: {path}"

def test_manifest_exists_and_format():
    path = "/home/user/manifest.json"
    assert os.path.isfile(path), f"Missing manifest file: {path}"

    with open(path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("manifest.json is not valid JSON.")

    assert isinstance(manifest, dict), "Manifest must be a JSON object (dictionary)."

    # Expected headers in hex
    expected_headers = [
        b'HEADER_A_1234567'.hex(),
        b'HEADER_B_9876543'.hex(),
        b'HEADER_C_0000000'.hex()
    ]

    for key, files in manifest.items():
        assert isinstance(key, str), "Keys in manifest must be strings."
        assert len(key) == 32, f"Key {key} is not a 16-byte hex string (32 chars)."
        assert key in expected_headers, f"Unexpected header hex key in manifest: {key}"
        assert isinstance(files, list), f"Value for key {key} must be an array of paths."
        for file_path in files:
            assert file_path.startswith("/app/raw_data/"), f"File path {file_path} is not an absolute path in /app/raw_data/"
            assert os.path.isabs(file_path), f"File path {file_path} is not absolute."

def test_zip_exists_and_size_metric():
    zip_path = "/home/user/organized.zip"
    assert os.path.isfile(zip_path), f"Missing ZIP archive: {zip_path}"

    size = os.path.getsize(zip_path)
    threshold = 2500000

    assert size <= threshold, f"ZIP archive size metric failed: {size} bytes > {threshold} bytes. Deduplication likely failed or was inefficient."

def test_zip_is_valid():
    zip_path = "/home/user/organized.zip"
    assert os.path.isfile(zip_path), f"Missing ZIP archive: {zip_path}"

    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            bad_file = z.testzip()
            assert bad_file is None, f"ZIP archive is corrupted. First bad file: {bad_file}"
    except zipfile.BadZipFile:
        pytest.fail("organized.zip is not a valid ZIP file.")