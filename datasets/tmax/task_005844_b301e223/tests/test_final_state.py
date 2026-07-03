# test_final_state.py

import os
import json
import hashlib
import pytest

def test_extracted_logs():
    extracted_dir = "/home/user/extracted_logs"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist."

    expected_files = {"batch_01.txt", "batch_02.txt"}
    actual_files = set(os.listdir(extracted_dir))

    assert expected_files.issubset(actual_files), f"Expected files {expected_files} not found in {extracted_dir}. Found: {actual_files}"

    for filename in expected_files:
        filepath = os.path.join(extracted_dir, filename)
        with open(filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                assert not line.startswith("!! DEBUG"), f"File {filepath} still contains '!! DEBUG' lines."

def test_parser_script_exists():
    parser_path = "/home/user/parser.py"
    assert os.path.isfile(parser_path), f"Python script {parser_path} does not exist."

def test_deploy_manifest():
    manifest_path = "/home/user/deploy_manifest.json"
    assert os.path.isfile(manifest_path), f"JSON manifest {manifest_path} does not exist."

    with open(manifest_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {manifest_path} is not valid JSON.")

    expected_data = {
        "/etc/nginx/nginx.conf": "f1e2d3c4b5a6",
        "/etc/systemd/system/myapp.service": "999988887777",
        "/etc/redis/redis.conf": "abcdefabcdef"
    }

    assert data == expected_data, f"JSON content in {manifest_path} does not match expected output.\nExpected: {expected_data}\nActual: {data}"

def test_manifest_checksum():
    manifest_path = "/home/user/deploy_manifest.json"
    checksum_path = "/home/user/manifest_checksum.txt"

    assert os.path.isfile(checksum_path), f"Checksum file {checksum_path} does not exist."
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist to verify checksum."

    with open(manifest_path, "rb") as f:
        actual_sha256 = hashlib.sha256(f.read()).hexdigest()

    with open(checksum_path, "r") as f:
        checksum_content = f.read().strip()

    # Standard sha256sum format: "<hash>  <filename>"
    # We just need to check if the correct hash is present at the beginning of the line
    assert checksum_content.startswith(actual_sha256), f"Checksum in {checksum_path} does not match the actual SHA256 of {manifest_path}.\nExpected hash starting with: {actual_sha256}\nActual content: {checksum_content}"