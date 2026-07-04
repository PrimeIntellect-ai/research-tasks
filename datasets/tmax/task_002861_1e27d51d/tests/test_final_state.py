# test_final_state.py

import os
import hashlib
import pytest

def test_workspace_exists():
    assert os.path.isdir("/home/user/workspace"), "The directory /home/user/workspace was not created."

def test_evil_links_deleted():
    evil1 = "/home/user/workspace/evil_link"
    evil2 = "/home/user/workspace/nested/evil_link2"
    assert not os.path.exists(evil1) and not os.path.islink(evil1), f"External symlink {evil1} was not deleted."
    assert not os.path.exists(evil2) and not os.path.islink(evil2), f"External symlink {evil2} was not deleted."

def test_safe_link_kept():
    safe_link = "/home/user/workspace/nested/safe_link.txt"
    assert os.path.islink(safe_link), f"Safe internal symlink {safe_link} was deleted or is not a symlink."

def test_binary_moved_and_renamed():
    binary_file = "/home/user/assets/image_data.bin"
    assert os.path.isfile(binary_file), f"Binary file was not moved to {binary_file}."

def test_text_files_renamed_and_converted():
    legacy_md = "/home/user/workspace/legacy.md"
    modern_md = "/home/user/workspace/nested/modern.md"

    assert os.path.isfile(legacy_md), f"Text file not renamed properly to {legacy_md}."
    assert os.path.isfile(modern_md), f"Text file not renamed properly to {modern_md}."

    # Check UTF-8 encoding
    try:
        with open(legacy_md, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "résumé, façade" in content, "Content of legacy file was lost or corrupted during conversion."
    except UnicodeDecodeError:
        pytest.fail(f"File {legacy_md} is not valid UTF-8.")

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def test_manifest():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} was not created."

    with open(manifest_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_files = [
        "/home/user/assets/image_data.bin",
        "/home/user/workspace/legacy.md",
        "/home/user/workspace/nested/modern.md"
    ]

    # Check that manifest is sorted alphabetically
    paths_in_manifest = [line.split(" | ")[0] for line in lines]
    assert paths_in_manifest == sorted(paths_in_manifest), "Manifest lines are not sorted alphabetically by absolute path."

    # Check completeness and correctness of hashes
    manifest_dict = {}
    for line in lines:
        parts = line.split(" | ")
        assert len(parts) == 2, f"Manifest line improperly formatted: {line}"
        manifest_dict[parts[0]] = parts[1]

    for expected_file in expected_files:
        assert expected_file in manifest_dict, f"File {expected_file} is missing from manifest."
        actual_hash = get_sha256(expected_file)
        assert manifest_dict[expected_file] == actual_hash, f"Hash mismatch in manifest for {expected_file}. Expected {actual_hash}, got {manifest_dict[expected_file]}."

    # Check that safe_link.txt is NOT in the manifest
    safe_link = "/home/user/workspace/nested/safe_link.txt"
    assert safe_link not in manifest_dict, f"Symlink {safe_link} should not be included in the manifest."