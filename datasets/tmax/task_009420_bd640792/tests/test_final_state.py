# test_final_state.py
import json
import os
import hashlib

def get_sha256(path):
    """Compute SHA-256 checksum of a file."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def test_final_manifest_exists_and_valid():
    manifest_path = "/home/user/final_manifest.json"
    assert os.path.exists(manifest_path), f"Output file {manifest_path} does not exist. Did your Rust program generate it?"

    with open(manifest_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{manifest_path} is not valid JSON."

    assert isinstance(data, list), "Manifest should be a JSON array."
    assert len(data) == 3, f"Expected exactly 3 valid entries in the manifest, but found {len(data)}."

    # Check that the list is sorted by ID ascending
    ids = [item.get("id") for item in data]
    assert all(isinstance(x, int) for x in ids), "All IDs should be integers."
    assert ids == sorted(ids), "The JSON array is not sorted by ID in ascending order."

    # Define the expected valid resolutions based on the corrupt manifest
    expected_entries = {
        8: "/home/user/artifacts/standard/beta.bin",
        45: "/home/user/artifacts/loop/alpha.bin",
        102: "/home/user/artifacts/standard/gamma.bin"
    }

    actual_entries = {item.get("id"): item for item in data}

    # Verify each expected entry
    for expected_id, expected_path in expected_entries.items():
        assert expected_id in actual_entries, f"Missing ID {expected_id} in final manifest. It should have been resolved and kept."
        item = actual_entries[expected_id]

        actual_path = item.get("canonical_path")
        assert actual_path == expected_path, f"Incorrect canonical path for ID {expected_id}. Expected {expected_path}, got {actual_path}."

        expected_sha = get_sha256(expected_path)
        actual_sha = item.get("sha256")
        assert actual_sha == expected_sha, f"Incorrect SHA256 for ID {expected_id}. Expected {expected_sha}, got {actual_sha}."

    # Verify that no unexpected IDs are present
    unexpected_ids = set(actual_entries.keys()) - set(expected_entries.keys())
    assert not unexpected_ids, f"Found unexpected IDs in the manifest: {unexpected_ids}. Ensure unverified or missing files are ignored, and duplicates are correctly overwritten by higher IDs."