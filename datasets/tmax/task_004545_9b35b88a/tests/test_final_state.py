# test_final_state.py
import os
import json
import hashlib
import pytest

CONFIG_PATH = "/home/user/config.json"

def get_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

@pytest.fixture(scope="module")
def config():
    assert os.path.exists(CONFIG_PATH), f"Config file missing at {CONFIG_PATH}"
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

@pytest.fixture(scope="module")
def bloated_data(config):
    source_dir = config.get("source_dir", "/home/user/bloated_data")
    assert os.path.isdir(source_dir), f"Source directory missing: {source_dir}"

    unique_hashes = {}
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.islink(filepath):
                continue
            file_hash = get_sha256(filepath)
            if file_hash not in unique_hashes:
                unique_hashes[file_hash] = []
            unique_hashes[file_hash].append(filepath)

    return unique_hashes

def test_manifest_exists_and_valid(config):
    manifest_path = config.get("manifest_path", "/home/user/manifest.json")
    assert os.path.exists(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    assert isinstance(manifest, list), "Manifest must be a JSON array"

def test_manifest_content_and_sorting(config, bloated_data):
    manifest_path = config.get("manifest_path", "/home/user/manifest.json")
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    assert len(manifest) == len(bloated_data), f"Expected {len(bloated_data)} unique files in manifest, got {len(manifest)}"

    new_filenames = [entry.get("new_filename", "") for entry in manifest]
    assert new_filenames == sorted(new_filenames), "Manifest entries are not sorted alphabetically by new_filename"

    manifest_hashes = set()
    for entry in manifest:
        orig_path = entry.get("original_path")
        new_name = entry.get("new_filename")
        sha256 = entry.get("sha256")

        assert orig_path, "Missing original_path in manifest entry"
        assert new_name, "Missing new_filename in manifest entry"
        assert sha256, "Missing sha256 in manifest entry"

        assert sha256 in bloated_data, f"Hash {sha256} from manifest not found in source data"
        assert orig_path in bloated_data[sha256], f"Original path {orig_path} does not match hash {sha256}"

        expected_new_name = f"{sha256[:8]}_{os.path.basename(orig_path)}"
        assert new_name == expected_new_name, f"Expected new_filename {expected_new_name}, got {new_name}"

        manifest_hashes.add(sha256)

    assert manifest_hashes == set(bloated_data.keys()), "Manifest does not cover all unique files"

def test_cleaned_data_directory(config, bloated_data):
    dest_dir = config.get("dest_dir", "/home/user/cleaned_data")
    assert os.path.isdir(dest_dir), f"Destination directory missing: {dest_dir}"

    manifest_path = config.get("manifest_path", "/home/user/manifest.json")
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    expected_files = {entry["new_filename"]: entry["sha256"] for entry in manifest}

    actual_files = os.listdir(dest_dir)
    assert len(actual_files) == len(expected_files), f"Expected {len(expected_files)} files in dest_dir, got {len(actual_files)}"

    for filename in actual_files:
        assert filename in expected_files, f"Unexpected file {filename} in dest_dir"
        filepath = os.path.join(dest_dir, filename)
        assert os.path.isfile(filepath), f"{filename} is not a regular file"

        actual_hash = get_sha256(filepath)
        assert actual_hash == expected_files[filename], f"Hash mismatch for copied file {filename}"