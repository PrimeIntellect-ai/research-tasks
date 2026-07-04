# test_final_state.py

import os
import json
import hashlib
import tarfile
import pytest

def test_manifest_exists_and_hashes_correct():
    manifest_path = "/home/user/docs_packaged/manifest.json"
    raw_dir = "/home/user/docs_raw"

    assert os.path.exists(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("manifest.json is not valid JSON")

    # Verify hashes in manifest
    files_checked = 0
    for root, _, files in os.walk(raw_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, raw_dir)
            # Using forward slashes for relative paths as required
            rel_path_fwd = rel_path.replace(os.sep, '/')

            with open(full_path, 'rb') as f:
                content = f.read()
                expected_hash = hashlib.sha256(content).hexdigest()

            assert rel_path_fwd in manifest, f"Missing {rel_path_fwd} in manifest.json"
            assert manifest[rel_path_fwd] == expected_hash, f"Hash mismatch for {rel_path_fwd}. Expected {expected_hash}, got {manifest[rel_path_fwd]}"
            files_checked += 1

    assert files_checked > 0, "No files were found in the raw directory to verify"

def test_archive_exists_and_contents_correct():
    archive_path = "/home/user/docs_packaged/archive.tar.gz"
    raw_dir = "/home/user/docs_raw"

    assert os.path.exists(archive_path), f"Archive file missing at {archive_path}"

    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            names = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"Archive at {archive_path} is not a valid gzip-compressed tarball")

    # Normalize names (remove leading ./)
    normalized_names = [name[2:] if name.startswith('./') else name for name in names]

    # Check that files exist and are not under docs_raw
    assert 'intro.md' in normalized_names, "Archive is missing intro.md at root"

    for name in normalized_names:
        assert not name.startswith('docs_raw/'), f"Archive contains docs_raw parent directory for '{name}', should be relative to docs_raw root"

    # Check that all files from raw_dir are in the archive
    for root, _, files in os.walk(raw_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, raw_dir)
            rel_path_fwd = rel_path.replace(os.sep, '/')

            assert rel_path_fwd in normalized_names, f"File {rel_path_fwd} is missing from the archive"