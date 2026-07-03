# test_final_state.py

import os
import json
import zipfile
import pytest

def test_extracted_directory_exists():
    assert os.path.isdir('/home/user/extracted'), "/home/user/extracted directory does not exist."

def test_corrupt_file_deleted():
    assert not os.path.exists('/home/user/extracted/fileC.bin'), "Corrupt file fileC.bin was not deleted."

def test_valid_files_renamed():
    expected_files = {
        'libnetwork_v2.bin',
        'core_engine_v15.bin'
    }
    extracted_files = set(os.listdir('/home/user/extracted'))

    for f in expected_files:
        assert f in extracted_files, f"Expected file {f} is missing from /home/user/extracted."

    assert 'fileA.bin' not in extracted_files, "Original fileA.bin was not renamed."
    assert 'fileB.bin' not in extracted_files, "Original fileB.bin was not renamed."

def test_registry_json_contents():
    registry_path = '/home/user/registry.json'
    assert os.path.isfile(registry_path), f"{registry_path} does not exist."

    with open(registry_path, 'r') as f:
        try:
            registry = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("registry.json is not valid JSON.")

    expected_registry = {
        "libnetwork_v2.bin": "fileA.bin",
        "core_engine_v15.bin": "fileB.bin"
    }

    assert registry == expected_registry, f"registry.json contents do not match expected mapping. Got: {registry}"

def test_curated_zip_contents():
    zip_path = '/home/user/curated.zip'
    assert os.path.isfile(zip_path), f"{zip_path} does not exist."

    assert zipfile.is_zipfile(zip_path), f"{zip_path} is not a valid zip archive."

    with zipfile.ZipFile(zip_path, 'r') as z:
        names = z.namelist()

    expected_names = {'libnetwork_v2.bin', 'core_engine_v15.bin'}

    # Check that exactly these files are in the zip, with no parent directories
    assert set(names) == expected_names, f"Zip contents do not match exactly. Expected {expected_names}, got {set(names)}."

    # Ensure no directories or paths are included
    for name in names:
        assert '/' not in name and '\\' not in name, f"File {name} in zip archive contains directory paths."