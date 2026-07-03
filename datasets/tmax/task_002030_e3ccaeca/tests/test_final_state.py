# test_final_state.py

import os
import hashlib
import pytest

DOCS_DIR = "/home/user/docs_draft"

def test_markdown_transformed():
    """Verify that the sed transformations were applied correctly to the markdown files."""
    intro_path = os.path.join(DOCS_DIR, "intro.md")
    assert os.path.isfile(intro_path), f"{intro_path} is missing"
    with open(intro_path, "r") as f:
        intro_content = f.read()
    assert "NOTE: Add architecture diagram" in intro_content, "intro.md was not transformed correctly (TODO -> NOTE)"
    assert "[DRAFT]" not in intro_content, "intro.md was not transformed correctly ([DRAFT] removal)"

    setup_path = os.path.join(DOCS_DIR, "setup.md")
    assert os.path.isfile(setup_path), f"{setup_path} is missing"
    with open(setup_path, "r") as f:
        setup_content = f.read()
    assert "NOTE: Verify permissions on step 3" in setup_content, "setup.md was not transformed correctly (TODO -> NOTE)"

    api_path = os.path.join(DOCS_DIR, "api.md")
    assert os.path.isfile(api_path), f"{api_path} is missing"
    with open(api_path, "r") as f:
        api_content = f.read()
    assert "NOTE: Document the /users endpoint" in api_content, "api.md was not transformed correctly (TODO -> NOTE)"
    assert "[DRAFT]" not in api_content, "api.md was not transformed correctly ([DRAFT] removal)"

def test_index_txt():
    """Verify that index.txt contains the correct titles for all markdown files."""
    index_path = os.path.join(DOCS_DIR, "index.txt")
    assert os.path.isfile(index_path), f"{index_path} is missing"

    with open(index_path, "r") as f:
        lines = sorted([line.strip() for line in f if line.strip()])

    expected = [
        "api.md: # API Reference",
        "intro.md: # Introduction to the System",
        "setup.md: # Installation Guide"
    ]

    assert lines == expected, f"index.txt content does not match expected. Found: {lines}"

def test_manifest_sha256():
    """Verify that manifest.sha256 exists and contains valid SHA256 sums for the files."""
    manifest_path = os.path.join(DOCS_DIR, "manifest.sha256")
    assert os.path.isfile(manifest_path), f"{manifest_path} is missing"

    with open(manifest_path, "r") as f:
        manifest_lines = [line.strip() for line in f if line.strip()]

    manifest_hashes = {}
    for line in manifest_lines:
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            # Handle potential '*' prefix for binary mode in sha256sum output
            filename = parts[1].lstrip("*")
            # Ensure it's just the filename, not an absolute path
            assert "/" not in filename, f"Manifest should contain relative filenames, found: {filename}"
            manifest_hashes[filename] = parts[0]

    expected_files = ["intro.md", "setup.md", "api.md", "index.txt"]

    for filename in expected_files:
        assert filename in manifest_hashes, f"{filename} is missing from manifest.sha256"

        filepath = os.path.join(DOCS_DIR, filename)
        assert os.path.isfile(filepath), f"{filepath} is missing"

        with open(filepath, "rb") as file_obj:
            actual_hash = hashlib.sha256(file_obj.read()).hexdigest()

        assert manifest_hashes[filename] == actual_hash, f"Hash mismatch in manifest for {filename}"