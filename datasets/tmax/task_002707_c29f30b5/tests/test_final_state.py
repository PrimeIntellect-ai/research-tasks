# test_final_state.py

import os
import hashlib
import pytest

SOURCE_DIR = "/home/user/source_data"
DEST_DIR = "/home/user/archive_dest"
MANIFEST_FILE = "/home/user/manifest.csv"

def get_expected_chunks():
    """Extracts, sorts, and chunks the critical lines exactly as specified."""
    critical_lines = []
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".log"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if "[CRITICAL]" in line:
                            critical_lines.append(line)

    # Sort alphabetically
    critical_lines.sort()

    # Split into chunks of 10 lines
    chunks = []
    for i in range(0, len(critical_lines), 10):
        chunks.append("".join(critical_lines[i:i+10]))

    return chunks

def get_chunk_filename(index):
    """Generates split-like suffixes: aa, ab, ac, etc."""
    return f"chunk_{chr(97 + (index // 26))}{chr(97 + (index % 26))}"

def test_archive_dest_exists():
    """Test that the destination directory was created."""
    assert os.path.isdir(DEST_DIR), f"Destination directory {DEST_DIR} was not created."

def test_chunk_files_correctness():
    """Test that the chunk files are correctly named and contain the correct sorted lines."""
    expected_chunks = get_expected_chunks()
    expected_files = {get_chunk_filename(i): content for i, content in enumerate(expected_chunks)}

    assert os.path.isdir(DEST_DIR), f"Destination directory {DEST_DIR} does not exist."
    actual_files = [f for f in os.listdir(DEST_DIR) if os.path.isfile(os.path.join(DEST_DIR, f))]

    assert sorted(actual_files) == sorted(expected_files.keys()), \
        f"Expected chunk files {sorted(expected_files.keys())}, but found {sorted(actual_files)} in {DEST_DIR}."

    for filename, expected_content in expected_files.items():
        file_path = os.path.join(DEST_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            actual_content = f.read()
        assert actual_content == expected_content, \
            f"Content of {filename} does not match the expected sorted and chunked lines."

def test_manifest_file_correctness():
    """Test that the manifest.csv is correctly formatted, hashed, and sorted."""
    assert os.path.isfile(MANIFEST_FILE), f"Manifest file {MANIFEST_FILE} was not created."

    expected_chunks = get_expected_chunks()
    expected_manifest_lines = []

    for i, content in enumerate(expected_chunks):
        filename = get_chunk_filename(i)
        sha256_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        expected_manifest_lines.append(f"{filename},{sha256_hash}")

    # Sort alphabetically by filename
    expected_manifest_lines.sort()

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        actual_manifest = f.read()

    # Clean up trailing newlines for robust comparison
    actual_lines = [line.strip() for line in actual_manifest.strip().split("\n") if line.strip()]
    expected_lines = [line.strip() for line in expected_manifest_lines]

    assert actual_lines == expected_lines, \
        f"Manifest file {MANIFEST_FILE} content does not match the expected sorted filenames and SHA256 hashes."