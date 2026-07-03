# test_final_state.py

import os
import hashlib
import re
import pytest

EXTRACTED_DOCS_DIR = "/home/user/extracted_docs"
MANIFEST_PATH = "/home/user/doc_manifest.txt"
SYMLINK_PATH = "/home/user/primary_doc.md"

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_extracted_docs_directory():
    """Check that the extracted_docs directory exists and contains exactly 5 files with correct naming."""
    assert os.path.exists(EXTRACTED_DOCS_DIR), f"Directory {EXTRACTED_DOCS_DIR} does not exist."
    assert os.path.isdir(EXTRACTED_DOCS_DIR), f"{EXTRACTED_DOCS_DIR} is not a directory."

    files = os.listdir(EXTRACTED_DOCS_DIR)
    assert len(files) == 5, f"Expected exactly 5 files in {EXTRACTED_DOCS_DIR}, found {len(files)}: {files}"

    for f in files:
        assert f.islower(), f"Filename '{f}' is not completely lowercase."
        assert " " not in f, f"Filename '{f}' contains spaces."
        assert f.endswith('.md') or f.endswith('.txt'), f"Filename '{f}' does not end with .md or .txt"

def test_conflict_resolution():
    """Ensure that the api_guide conflict was resolved (two files present)."""
    files = os.listdir(EXTRACTED_DOCS_DIR)
    api_guides = [f for f in files if f.startswith('api_guide') and f.endswith('.md')]
    assert len(api_guides) == 2, f"Expected 2 variants of 'api_guide.md' due to conflict resolution, found: {api_guides}"

def test_manifest_generation():
    """Check that the manifest exists, is sorted, and contains valid hashes."""
    assert os.path.exists(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."
    assert os.path.isfile(MANIFEST_PATH), f"{MANIFEST_PATH} is not a file."

    with open(MANIFEST_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Manifest should contain exactly 5 lines, found {len(lines)}."

    filenames_in_manifest = []
    for line in lines:
        parts = re.split(r'\s+', line, maxsplit=1)
        assert len(parts) == 2, f"Manifest line '{line}' is not in standard format."
        file_hash, filename = parts

        # Strip leading asterisk or space if standard sha256sum format
        if filename.startswith('*') or filename.startswith(' '):
            filename = filename[1:]

        # Extract base filename if path was included
        base_filename = os.path.basename(filename)
        filenames_in_manifest.append(base_filename)

        actual_path = os.path.join(EXTRACTED_DOCS_DIR, base_filename)
        assert os.path.exists(actual_path), f"File {base_filename} listed in manifest does not exist in {EXTRACTED_DOCS_DIR}."

        expected_hash = get_sha256(actual_path)
        assert file_hash == expected_hash, f"Hash mismatch for {base_filename}. Expected {expected_hash}, got {file_hash}."

    # Check if manifest is sorted alphabetically by filename
    assert filenames_in_manifest == sorted(filenames_in_manifest), "Manifest lines are not sorted alphabetically by filename."

def test_symlink_largest_file():
    """Check that primary_doc.md is a symlink to the largest file."""
    assert os.path.exists(SYMLINK_PATH), f"Symlink {SYMLINK_PATH} does not exist."
    assert os.path.islink(SYMLINK_PATH), f"{SYMLINK_PATH} is not a symbolic link."

    # Find the largest file in the directory
    files = os.listdir(EXTRACTED_DOCS_DIR)
    largest_file = None
    max_size = -1
    for f in files:
        filepath = os.path.join(EXTRACTED_DOCS_DIR, f)
        size = os.path.getsize(filepath)
        if size > max_size:
            max_size = size
            largest_file = filepath

    target_path = os.path.realpath(SYMLINK_PATH)
    largest_file_real = os.path.realpath(largest_file)

    assert target_path == largest_file_real, f"Symlink points to {target_path}, but the largest file is {largest_file_real}."