# test_final_state.py

import os
import hashlib
import re

STAGING_DIR = '/home/user/docs_staging'
MANIFEST_PATH = '/home/user/manifest.txt'
SCRIPT_PATH = '/home/user/build_manifest.py'

def test_files_extracted():
    """Verify that the archive was extracted to the correct location."""
    assert os.path.exists(STAGING_DIR), f"Directory {STAGING_DIR} does not exist."
    assert os.path.isdir(STAGING_DIR), f"{STAGING_DIR} is not a directory."

    expected_files = [
        'intro.md',
        'api/auth.md',
        'setup/install.md',
        'setup/notes.txt'
    ]
    for f in expected_files:
        full_path = os.path.join(STAGING_DIR, f)
        assert os.path.exists(full_path), f"Expected file {full_path} is missing."

def test_markdown_files_updated():
    """Verify that all markdown files have 'alpha' replaced with 'stable'."""
    md_files = [
        'intro.md',
        'api/auth.md',
        'setup/install.md'
    ]
    for f in md_files:
        full_path = os.path.join(STAGING_DIR, f)
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
            assert 'ProductX-v1.0-alpha' not in content, f"File {f} still contains 'ProductX-v1.0-alpha'."
            assert 'ProductX-v1.0-stable' in content, f"File {f} does not contain 'ProductX-v1.0-stable'."

def test_txt_files_unchanged():
    """Verify that non-markdown files were not modified."""
    txt_path = os.path.join(STAGING_DIR, 'setup/notes.txt')
    with open(txt_path, 'r', encoding='utf-8') as file:
        content = file.read()
        assert 'ProductX-v1.0-alpha' in content, "The file setup/notes.txt should not have been modified, but 'ProductX-v1.0-alpha' is missing."
        assert 'ProductX-v1.0-stable' not in content, "The file setup/notes.txt should not contain 'ProductX-v1.0-stable'."

def test_manifest_generated_correctly():
    """Verify the manifest.txt format and contents."""
    assert os.path.exists(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

    expected_md_files = [
        'api/auth.md',
        'intro.md',
        'setup/install.md'
    ]

    # Calculate expected hashes dynamically
    expected_entries = []
    for rel_path in expected_md_files:
        full_path = os.path.join(STAGING_DIR, rel_path)
        with open(full_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        expected_entries.append(f"{file_hash}  {rel_path}")

    # Read actual manifest
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_entries), f"Manifest should have exactly {len(expected_entries)} entries, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_entries)):
        assert actual == expected, f"Manifest line {i+1} is incorrect.\nExpected: '{expected}'\nFound:    '{actual}'"

def test_script_exists():
    """Verify that the build_manifest.py script was created."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a regular file."