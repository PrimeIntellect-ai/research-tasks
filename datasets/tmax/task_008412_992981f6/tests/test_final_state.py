# test_final_state.py

import os
import hashlib
import pytest

def get_sha256(filepath):
    """Calculate the SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_zip_slip_prevention():
    """Verify that the Zip Slip vulnerability was prevented."""
    escaped_file = "/home/user/escaped.json"
    assert not os.path.exists(escaped_file), (
        f"Vulnerability not patched: The file {escaped_file} was extracted "
        "outside the intended directory."
    )

def test_files_extracted_correctly():
    """Verify that the safe files were extracted to the correct location."""
    main_json = "/home/user/configs/main.json"
    sub_db_json = "/home/user/configs/sub/db.json"

    assert os.path.isfile(main_json), f"Expected extracted file missing: {main_json}"
    assert os.path.isfile(sub_db_json), f"Expected extracted file missing: {sub_db_json}"

    # Verify contents match expected setup
    with open(main_json, "r") as f:
        assert '{"version": 1}' in f.read(), f"Content mismatch in {main_json}"

    with open(sub_db_json, "r") as f:
        assert '{"db": "mysql"}' in f.read(), f"Content mismatch in {sub_db_json}"

def test_manifest_correctness():
    """Verify the SHA-256 manifest is correctly generated and sorted."""
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    main_json_path = "/home/user/configs/main.json"
    sub_db_json_path = "/home/user/configs/sub/db.json"

    # Recompute hashes from the actual files to be robust
    expected_main_hash = get_sha256(main_json_path) if os.path.exists(main_json_path) else "MISSING"
    expected_sub_hash = get_sha256(sub_db_json_path) if os.path.exists(sub_db_json_path) else "MISSING"

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Manifest should contain exactly 2 entries, found {len(lines)}"

    # Parse the actual manifest lines
    parsed_manifest = {}
    for line in lines:
        parts = line.split(None, 1)  # split on whitespace, max 1 split
        assert len(parts) == 2, f"Invalid manifest line format: '{line}'"
        hash_val, filename = parts
        # Allow for optional leading './' in filenames
        if filename.startswith('./'):
            filename = filename[2:]
        parsed_manifest[filename] = hash_val

    assert "main.json" in parsed_manifest, "Manifest is missing entry for main.json"
    assert "sub/db.json" in parsed_manifest, "Manifest is missing entry for sub/db.json"

    assert parsed_manifest["main.json"] == expected_main_hash, "Hash mismatch for main.json in manifest"
    assert parsed_manifest["sub/db.json"] == expected_sub_hash, "Hash mismatch for sub/db.json in manifest"

    # Verify sorting (alphabetical by filename according to standard sha256sum output)
    # The truth expects main.json first, then sub/db.json
    assert lines[0].endswith("main.json"), "Manifest is not sorted alphabetically by filename (expected main.json first)"
    assert lines[1].endswith("db.json"), "Manifest is not sorted alphabetically by filename (expected sub/db.json second)"