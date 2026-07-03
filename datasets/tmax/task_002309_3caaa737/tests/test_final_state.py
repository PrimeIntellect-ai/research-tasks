# test_final_state.py

import os
import tarfile
import hashlib
import pytest

WORKSPACE_DIR = "/home/user/project_workspace"
MANIFEST_PATH = "/home/user/manifest.sha256"
CLEAN_ARCHIVE = "/home/user/clean_project.tar.gz"

def get_all_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def test_workspace_exists():
    assert os.path.exists(WORKSPACE_DIR), f"Workspace directory {WORKSPACE_DIR} does not exist."
    assert os.path.isdir(WORKSPACE_DIR), f"{WORKSPACE_DIR} is not a directory."

def test_text_files_utf8_encoded():
    # Find all .txt files and ensure they can be read as UTF-8
    txt_files = [f for f in get_all_files(WORKSPACE_DIR) if f.endswith('.txt')]
    assert len(txt_files) > 0, "No .txt files found in the workspace."

    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            # Also verify it's not empty and doesn't contain replacement characters if possible,
            # but reading successfully without UnicodeDecodeError is the main check.
        except UnicodeDecodeError:
            pytest.fail(f"File {txt_file} is not valid UTF-8.")

def test_hardlinks_created_for_duplicates():
    # The setup created identical CSV files.
    # docs/data_copy.csv, src/data.csv, src/data_backup.csv
    file1 = os.path.join(WORKSPACE_DIR, "docs/data_copy.csv")
    file2 = os.path.join(WORKSPACE_DIR, "src/data.csv")
    file3 = os.path.join(WORKSPACE_DIR, "src/data_backup.csv")

    assert os.path.exists(file1), f"{file1} is missing."
    assert os.path.exists(file2), f"{file2} is missing."
    assert os.path.exists(file3), f"{file3} is missing."

    stat1 = os.stat(file1)
    stat2 = os.stat(file2)
    stat3 = os.stat(file3)

    assert stat1.st_ino == stat2.st_ino, f"{file1} and {file2} are not hardlinked."
    assert stat1.st_ino == stat3.st_ino, f"{file1} and {file3} are not hardlinked."

    # Check that they have 3 hard links
    assert stat1.st_nlink >= 3, f"Expected at least 3 hardlinks for the duplicate files, got {stat1.st_nlink}."

def test_manifest_format_and_correctness():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, "Manifest file is empty."

    # Calculate expected hashes
    expected_entries = []
    for filepath in get_all_files(WORKSPACE_DIR):
        rel_path = "./" + os.path.relpath(filepath, WORKSPACE_DIR)
        with open(filepath, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        expected_entries.append(f"{file_hash}  {rel_path}")

    expected_entries.sort()

    # Ensure the manifest matches exactly
    assert lines == expected_entries, "Manifest contents do not match expected hashes, format, or sorting."

def test_clean_archive_structure():
    assert os.path.exists(CLEAN_ARCHIVE), f"Clean archive {CLEAN_ARCHIVE} does not exist."
    assert tarfile.is_tarfile(CLEAN_ARCHIVE), f"{CLEAN_ARCHIVE} is not a valid tar archive."

    with tarfile.open(CLEAN_ARCHIVE, 'r:gz') as tar:
        members = tar.getnames()

    assert len(members) > 0, "Clean archive is empty."

    for member in members:
        # The archive should not have a top-level project_workspace directory
        # Paths should be like 'docs/...', 'src/...', or './docs/...'
        parts = member.split('/')
        if parts[0] == '.':
            parts = parts[1:]
        if parts:
            assert parts[0] != "project_workspace", f"Archive contains top-level project_workspace directory: {member}"