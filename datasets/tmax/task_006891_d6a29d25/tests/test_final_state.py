# test_final_state.py

import os
import subprocess
import hashlib

def test_cpp_file_exists():
    cpp_file = "/home/user/split_assets.cpp"
    assert os.path.isfile(cpp_file), f"Expected C++ source file {cpp_file} does not exist."

def test_output_files_exist_and_sizes():
    expected_files = {
        "level1.bin": 2048,
        "level2.bin": 4096,
        "sprites.bin": 1024,
        "audio.bin": 2048,
        "remainder.bin": 1024
    }

    for filename, expected_size in expected_files.items():
        filepath = f"/home/user/output/{filename}"
        assert os.path.isfile(filepath), f"Expected output file {filepath} does not exist."
        actual_size = os.path.getsize(filepath)
        assert actual_size == expected_size, f"File {filepath} should be {expected_size} bytes, but is {actual_size} bytes."

def test_concatenated_content_matches_original():
    files_in_order = [
        "/home/user/output/level1.bin",
        "/home/user/output/level2.bin",
        "/home/user/output/sprites.bin",
        "/home/user/output/audio.bin",
        "/home/user/output/remainder.bin"
    ]

    concatenated_data = bytearray()
    for filepath in files_in_order:
        assert os.path.isfile(filepath), f"Missing file for concatenation: {filepath}"
        with open(filepath, "rb") as f:
            concatenated_data.extend(f.read())

    original_data_file = "/home/user/project_data.bin"
    assert os.path.isfile(original_data_file), f"Original data file {original_data_file} is missing."

    with open(original_data_file, "rb") as f:
        original_data = f.read()

    assert concatenated_data == original_data, "The concatenated output files do not match the original project_data.bin."

def test_manifest_sha256():
    manifest_file = "/home/user/output/manifest.sha256"
    assert os.path.isfile(manifest_file), f"Manifest file {manifest_file} does not exist."

    expected_files = [
        "level1.bin",
        "level2.bin",
        "sprites.bin",
        "audio.bin",
        "remainder.bin"
    ]

    # Check that manifest succeeds with sha256sum
    result = subprocess.run(
        ["sha256sum", "-c", "manifest.sha256"],
        cwd="/home/user/output",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"sha256sum validation failed. Output:\n{result.stdout}\n{result.stderr}"

    # Check that all expected files are mentioned in the manifest
    with open(manifest_file, "r") as f:
        manifest_content = f.read()

    for filename in expected_files:
        assert filename in manifest_content, f"File {filename} is missing from the manifest."