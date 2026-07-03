# test_final_state.py

import os
import json
import pytest

def test_published_directory_exists():
    curated_dir = "/home/user/published/release_1_curated"
    assert os.path.isdir(curated_dir), f"The directory {curated_dir} does not exist. Did the script publish the artifacts?"

def test_published_files_exist():
    curated_dir = "/home/user/published/release_1_curated"
    expected_files = ["binary.elf", "signature.bin", "metadata.json"]
    for f in expected_files:
        file_path = os.path.join(curated_dir, f)
        assert os.path.isfile(file_path), f"Expected file {f} is missing in {curated_dir}."

def test_binary_and_signature_contents():
    curated_dir = "/home/user/published/release_1_curated"

    sig_path = os.path.join(curated_dir, "signature.bin")
    if os.path.exists(sig_path):
        with open(sig_path, "r") as f:
            assert f.read() == "SIG-12345", "The content of signature.bin is incorrect."

    bin_path = os.path.join(curated_dir, "binary.elf")
    if os.path.exists(bin_path):
        with open(bin_path, "r") as f:
            assert f.read() == "ELF-DATA", "The content of binary.elf is incorrect."

def test_metadata_json_content():
    json_path = "/home/user/published/release_1_curated/metadata.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    expected_data = {
        "build": {
            "version": "1.0.42",
            "arch": "amd64"
        },
        "runtime": {
            "env": "production"
        }
    }

    assert data == expected_data, f"The contents of {json_path} do not match the expected parsed INI structure."

def test_success_log_exists_and_matches():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist. Did you copy the metadata.json file?"

    with open(log_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{log_path} does not contain valid JSON.")

    expected_data = {
        "build": {
            "version": "1.0.42",
            "arch": "amd64"
        },
        "runtime": {
            "env": "production"
        }
    }

    assert data == expected_data, f"The contents of {log_path} do not match the expected JSON output."