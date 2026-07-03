# test_final_state.py

import os
import json
import hashlib
import pytest

def test_backup_archive_size():
    archive_path = '/app/diff_backup.tar.gz'
    assert os.path.exists(archive_path), f"Backup archive missing at {archive_path}"

    archive_size = os.path.getsize(archive_path)
    # The metric threshold is 10240 bytes (10 KB)
    assert archive_size <= 10240, f"Archive too large: {archive_size} bytes. Expected <= 10240 bytes. You likely backed up unmodified files."

def test_manifest_and_replacements():
    manifest_path = '/app/manifest.json'
    assert os.path.exists(manifest_path), f"Manifest missing at {manifest_path}"

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    assert isinstance(manifest, dict), "Manifest must be a JSON dictionary mapping relative paths to checksums"
    assert len(manifest) == 10, f"Expected exactly 10 modified files in manifest, got {len(manifest)}"

    for rel_path, expected_hash in manifest.items():
        full_path = os.path.join('/app/messy_project', rel_path)
        assert os.path.exists(full_path), f"File referenced in manifest missing: {full_path}"

        with open(full_path, 'rb') as f:
            file_bytes = f.read()
            actual_hash = hashlib.sha256(file_bytes).hexdigest()

        assert actual_hash == expected_hash, f"SHA256 hash mismatch for {rel_path}. Expected {expected_hash}, got {actual_hash}"

        content = file_bytes.decode('utf-8', errors='replace')
        assert 'SECURE_KEY_7741_VX' in content, f"Replacement string 'SECURE_KEY_7741_VX' missing in {rel_path}"
        assert 'OLD_API_KEY_992' not in content, f"Old key 'OLD_API_KEY_992' still present in {rel_path}"