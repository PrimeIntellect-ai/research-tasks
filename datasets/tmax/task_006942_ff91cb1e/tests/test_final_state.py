# test_final_state.py

import os
import json
import pytest

DOCS_OUTPUT_DIR = "/home/user/docs_output"

def test_output_directory_exists():
    """Verify that the docs_output directory was created."""
    assert os.path.isdir(DOCS_OUTPUT_DIR), f"Directory {DOCS_OUTPUT_DIR} does not exist."

def test_decoded_files_content():
    """Verify that the decoded files exist with the correct content."""
    expected_files = {
        "malicious.txt": b"Hello world!",
        "setup.md": b"# Setup\n\nRun the script.",
        "api_ref.csv": b"ID,NAME\n1,Alice\n2,Bob\n"
    }

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(DOCS_OUTPUT_DIR, filename)
        assert os.path.isfile(filepath), f"Expected file {filepath} is missing."

        with open(filepath, 'rb') as f:
            content = f.read()

        assert content == expected_content, f"Content of {filepath} is incorrect."

def test_manifest_json():
    """Verify that manifest.json exists and contains correct file lengths."""
    manifest_path = os.path.join(DOCS_OUTPUT_DIR, "manifest.json")
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{manifest_path} is not a valid JSON file.")

    expected_manifest = {
        "malicious.txt": 12,
        "setup.md": 24,
        "api_ref.csv": 22
    }

    assert manifest == expected_manifest, f"Manifest content {manifest} does not match expected {expected_manifest}."

def test_no_tmp_files():
    """Verify that no temporary files were left behind in the output directory."""
    if not os.path.isdir(DOCS_OUTPUT_DIR):
        pytest.skip("Output directory missing.")

    for filename in os.listdir(DOCS_OUTPUT_DIR):
        assert not filename.endswith(".tmp"), f"Temporary file left behind: {filename}"

def test_no_directory_traversal():
    """Verify that the script did not write files outside the intended directory."""
    traversal_path = "/home/user/malicious.txt"
    assert not os.path.isfile(traversal_path), f"Directory traversal vulnerability exploited! File found at {traversal_path}."