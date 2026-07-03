# test_final_state.py
import json
import hashlib
import os
import pytest

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def test_manifest_accuracy():
    manifest_path = '/home/user/manifest.json'
    assert os.path.exists(manifest_path), f"Manifest file missing: {manifest_path}"

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to parse manifest.json: {e}")

    expected_files = {
        "intro_part1.txt": 1000,
        "intro_part2.txt": 1000,
        "intro_part3.txt": 500,
        "guide.txt": 2000
    }

    correct_count = 0
    assert isinstance(manifest, list), "Manifest JSON should be a list of objects"

    manifest_dict = {item.get("filename"): item.get("hash") for item in manifest if isinstance(item, dict)}

    for fname, size in expected_files.items():
        fpath = os.path.join('/home/user/docs', fname)
        assert os.path.exists(fpath), f"Expected file missing: {fpath}"

        actual_size = os.path.getsize(fpath)
        assert actual_size == size, f"File {fname} has incorrect size: {actual_size} bytes (expected {size} bytes)"

        actual_hash = hash_file(fpath)
        manifest_hash = manifest_dict.get(fname)
        assert manifest_hash == actual_hash, f"Hash mismatch or missing for {fname} in manifest. Expected {actual_hash}, got {manifest_hash}"

        correct_count += 1

    accuracy = correct_count / len(expected_files)
    assert accuracy >= 1.0, f"Accuracy metric failed: {accuracy} < 1.0"