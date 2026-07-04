# test_final_state.py

import json
import os
import pytest

TARGET_DIR = "/home/user/artifacts_curated"

EXPECTED_JSON = {
    "art_001.json": {"id": "art_001", "payload_file": "data1.bin"},
    "omega_42.json": {"id": "omega_42", "payload_file": "payload.dat"},
    "zeta_77.json": {"id": "zeta_77", "payload_file": "core.dump"}
}

EXPECTED_BIN = {
    "art_001.bin": b"CURATED_\x01\x02\x03\x04\x0A\x0B\x0C",
    "omega_42.bin": b"CURATED_\xFF\xEE\xDD\xCC\xBB\xAA",
    "zeta_77.bin": b"CURATED_\x00\x00\x00\x00\x42\x42"
}

def test_target_directory_exists():
    assert os.path.isdir(TARGET_DIR), f"Target directory {TARGET_DIR} does not exist. Did you run the script?"

@pytest.mark.parametrize("fname, expected_data", EXPECTED_JSON.items())
def test_json_files(fname, expected_data):
    file_path = os.path.join(TARGET_DIR, fname)
    assert os.path.isfile(file_path), f"Expected JSON file {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    assert data == expected_data, f"Data in {file_path} does not match expected output."

@pytest.mark.parametrize("fname, expected_data", EXPECTED_BIN.items())
def test_binary_files(fname, expected_data):
    file_path = os.path.join(TARGET_DIR, fname)
    assert os.path.isfile(file_path), f"Expected binary file {file_path} is missing."

    with open(file_path, 'rb') as f:
        data = f.read()

    assert data.startswith(b"CURATED_"), f"Binary file {file_path} does not start with 'CURATED_'."
    assert data == expected_data, f"Binary data in {file_path} does not match the expected modified payload."