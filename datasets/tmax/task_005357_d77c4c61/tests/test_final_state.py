# test_final_state.py

import os
import json
import hashlib
import pytest

def test_extract_docs_script_exists():
    """Verify that the user created the extraction script."""
    script_path = "/home/user/extract_docs.py"
    assert os.path.isfile(script_path), f"Python script is missing at {script_path}"

def test_output_dir_exists():
    """Verify that the output directory was created."""
    output_dir = "/home/user/extracted_docs"
    assert os.path.isdir(output_dir), f"Expected output directory {output_dir} does not exist."

def test_extracted_files_exist_and_flattened():
    """Verify that all files were extracted to the output directory with flattened paths."""
    output_dir = "/home/user/extracted_docs"
    expected_files = {"intro.md", "logo.png", "passwd_override.txt"}

    if not os.path.isdir(output_dir):
        pytest.fail(f"Output directory {output_dir} missing, cannot check files.")

    actual_files = set(os.listdir(output_dir))
    assert actual_files == expected_files, f"Extracted files do not match expected. Expected {expected_files}, got {actual_files}"

def test_no_directory_traversal():
    """Verify that zip-slip mitigation worked and files weren't extracted outside the output dir."""
    bad_path_1 = "/home/user/etc/passwd_override.txt"
    bad_path_2 = "/etc/passwd_override.txt"

    assert not os.path.exists(bad_path_1), f"Directory traversal occurred: file written to {bad_path_1}"
    assert not os.path.exists(bad_path_2), f"Directory traversal occurred: file written to {bad_path_2}"

def test_manifest_json_correct():
    """Verify that the manifest.json file exists and contains the correct mapping."""
    manifest_path = "/home/user/manifest.json"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{manifest_path} is not valid JSON.")

    expected_hashes = {
        "intro.md": "ab2221650bde48644ed1bd1710817c1815147bf140228e3b7b99ba14c4da4397",
        "logo.png": "e11505bd27bb9480cf890f845a7bdc31aef70bc3caebbb12eb36cb07ed564b07",
        "passwd_override.txt": "76ab5a8e2cc89d363717ea2a514d7dcdd9ba33de8e762c2f60d6964a2bd017c6"
    }

    assert manifest == expected_hashes, f"Manifest contents do not match expected. Got: {manifest}"

def test_extracted_file_contents_match():
    """Verify that the extracted files have the correct contents matching the expected hashes."""
    expected_hashes = {
        "intro.md": "ab2221650bde48644ed1bd1710817c1815147bf140228e3b7b99ba14c4da4397",
        "logo.png": "e11505bd27bb9480cf890f845a7bdc31aef70bc3caebbb12eb36cb07ed564b07",
        "passwd_override.txt": "76ab5a8e2cc89d363717ea2a514d7dcdd9ba33de8e762c2f60d6964a2bd017c6"
    }

    for filename, expected_hash in expected_hashes.items():
        filepath = os.path.join("/home/user/extracted_docs", filename)
        assert os.path.isfile(filepath), f"File {filename} is missing from output directory."

        with open(filepath, "rb") as f:
            content = f.read()
            actual_hash = hashlib.sha256(content).hexdigest()

        assert actual_hash == expected_hash, f"Hash mismatch for {filename}. Expected {expected_hash}, got {actual_hash}"