# test_final_state.py

import os
import hashlib
import pytest

DOCS_DIR = "/home/user/docs"
MANIFEST_PATH = os.path.join(DOCS_DIR, "manifest.sha256")

def test_published_md_files_updated():
    published_files = ["intro.md", "setup.md"]
    for filename in published_files:
        filepath = os.path.join(DOCS_DIR, filename)
        assert os.path.isfile(filepath), f"Expected file {filepath} is missing."
        with open(filepath, "r") as f:
            content = f.read()
        assert "NovaBrand" in content, f"File {filename} should contain 'NovaBrand'."
        assert "LegacyBrand" not in content, f"File {filename} should no longer contain 'LegacyBrand'."

def test_draft_md_files_unchanged():
    filepath = os.path.join(DOCS_DIR, "draft_api.md")
    assert os.path.isfile(filepath), f"Expected file {filepath} is missing."
    with open(filepath, "r") as f:
        content = f.read()
    assert "LegacyBrand" in content, f"File draft_api.md should still contain 'LegacyBrand'."
    assert "NovaBrand" not in content, f"File draft_api.md should not contain 'NovaBrand'."

def test_non_md_files_unchanged():
    filepath = os.path.join(DOCS_DIR, "notes.txt")
    assert os.path.isfile(filepath), f"Expected file {filepath} is missing."
    with open(filepath, "r") as f:
        content = f.read()
    assert "LegacyBrand" in content, f"File notes.txt should still contain 'LegacyBrand'."
    assert "NovaBrand" not in content, f"File notes.txt should not contain 'NovaBrand'."

def test_manifest_exists_and_correct():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} is missing."

    with open(MANIFEST_PATH, "r") as f:
        manifest_lines = f.read().strip().splitlines()

    assert len(manifest_lines) == 2, f"Manifest should contain exactly 2 entries, found {len(manifest_lines)}."

    parsed_manifest = {}
    for line in manifest_lines:
        parts = line.strip().split(maxsplit=1)
        assert len(parts) == 2, f"Invalid manifest line format: '{line}'"
        hash_val, filename = parts
        # some tools prepend a '*' or ' ' to the filename in sha256sum output
        filename = filename.lstrip(" *")
        parsed_manifest[os.path.basename(filename)] = hash_val

    expected_files = ["intro.md", "setup.md"]
    for filename in expected_files:
        assert filename in parsed_manifest, f"Manifest is missing entry for {filename}."

        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, "rb") as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()

        assert parsed_manifest[filename] == actual_hash, f"Hash mismatch in manifest for {filename}."