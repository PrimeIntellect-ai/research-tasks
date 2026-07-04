# test_final_state.py
import os
import json
import struct
import zipfile
import hashlib
import tempfile
import pytest

def create_bx_bytes(magic=b'BX01', version=2, payload=b""):
    """Helper to generate the bytes of a valid .bx file for hashing."""
    data = bytearray()
    data.extend(magic)
    data.extend(struct.pack('<H', version))
    data.extend(struct.pack('<I', len(payload)))
    data.extend(payload)
    return bytes(data)

def get_expected_valid_artifacts():
    """Returns a dict of expected sha256 -> (original_basename, file_bytes)"""
    expected = [
        ("valid1.bx", b"hello world"),
        ("valid2.bx", b"rust programming is fun!"),
        ("zip_valid.bx", b"inside zip file"),
        ("tar_valid.bx", b"inside tar gz"),
    ]

    artifacts = {}
    for basename, payload in expected:
        file_bytes = create_bx_bytes(payload=payload)
        sha256_hash = hashlib.sha256(file_bytes).hexdigest()
        artifacts[f"{sha256_hash}.bx"] = (basename, file_bytes)

    return artifacts

def test_curated_release_zip_exists():
    zip_path = "/home/user/curated_release.zip"
    assert os.path.isfile(zip_path), f"Expected release archive not found at {zip_path}"
    assert zipfile.is_zipfile(zip_path), f"{zip_path} is not a valid zip file"

def test_curated_release_contents():
    zip_path = "/home/user/curated_release.zip"
    if not os.path.isfile(zip_path) or not zipfile.is_zipfile(zip_path):
        pytest.skip("Release zip missing or invalid")

    expected_artifacts = get_expected_valid_artifacts()

    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(tmpdir)

        # Find manifest.json
        manifest_path = None
        for root, dirs, files in os.walk(tmpdir):
            if "manifest.json" in files:
                manifest_path = os.path.join(root, "manifest.json")
                break

        assert manifest_path is not None, "manifest.json not found in the release zip"

        with open(manifest_path, 'r') as f:
            try:
                manifest = json.load(f)
            except json.JSONDecodeError:
                pytest.fail("manifest.json is not valid JSON")

        assert isinstance(manifest, dict), "manifest.json must contain a JSON object"

        # Check manifest keys and values
        expected_keys = set(expected_artifacts.keys())
        actual_keys = set(manifest.keys())

        missing_keys = expected_keys - actual_keys
        extra_keys = actual_keys - expected_keys

        assert not missing_keys, f"Manifest is missing expected entries: {missing_keys}"
        assert not extra_keys, f"Manifest contains unexpected entries: {extra_keys}"

        for hashed_name, (basename, _) in expected_artifacts.items():
            assert manifest[hashed_name] == basename, f"Manifest mapping for {hashed_name} should be {basename}, got {manifest[hashed_name]}"

        # Check the actual .bx files in the zip
        manifest_dir = os.path.dirname(manifest_path)
        for hashed_name, (_, expected_bytes) in expected_artifacts.items():
            file_path = os.path.join(manifest_dir, hashed_name)
            assert os.path.isfile(file_path), f"Expected file {hashed_name} not found in the same directory as manifest.json"

            with open(file_path, 'rb') as f:
                actual_bytes = f.read()

            assert actual_bytes == expected_bytes, f"Contents of {hashed_name} do not match the expected .bx format and payload"