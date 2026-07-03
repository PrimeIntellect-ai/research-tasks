# test_final_state.py

import os
import pytest

def test_extracted_files_content():
    """Verify the safe files are extracted and [COMPANY_NAME] is replaced with AcmeCorp in .md files."""

    expected_files = {
        "/home/user/docs_safe/intro.md": "# Welcome to AcmeCorp Docs\nThis is the intro.",
        "/home/user/docs_safe/api/setup.md": "## API Setup\nAcmeCorp provides a REST API.",
        "/home/user/docs_safe/internal/notes.txt": "Random notes. No company name here."
    }

    for path, expected_content in expected_files.items():
        assert os.path.isfile(path), f"Expected file {path} is missing."
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == expected_content, f"Content mismatch in {path}."

def test_malicious_files_skipped():
    """Verify that files with '../' in their path were not extracted."""

    # Paths that would have been created if directory traversal succeeded
    malicious_paths = [
        "/home/user/hacked_root.md",
        "/home/etc_fake/passwd",
        "/home/user/sneaky.md",
        # Also check they weren't somehow extracted literally with '../' in the name if filesystem allows
        "/home/user/docs_safe/../hacked_root.md",
        "/home/user/docs_safe/api/../../etc_fake/passwd",
        "/home/user/docs_safe/nested/../../sneaky.md"
    ]

    for path in malicious_paths:
        # Resolve path to handle any literal '..' if they were created
        resolved_path = os.path.abspath(path)
        assert not os.path.exists(resolved_path), f"Malicious file {resolved_path} was extracted!"

def test_manifest_file():
    """Verify that the manifest file is generated correctly with sorted relative paths."""
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    with open(manifest_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "api/setup.md",
        "internal/notes.txt",
        "intro.md"
    ]

    assert lines == expected_lines, f"Manifest content mismatch. Expected {expected_lines}, got {lines}."