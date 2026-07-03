# test_final_state.py

import os
import json
import hashlib
import pytest

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_script_exists_and_executable():
    script_path = "/home/user/curator.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_repo_structure_exists():
    assert os.path.isdir("/home/user/repo/artifacts"), "/home/user/repo/artifacts directory does not exist."
    assert os.path.isfile("/home/user/repo/manifest.json"), "/home/user/repo/manifest.json does not exist."

def test_manifest_contents_and_sharded_files():
    manifest_path = "/home/user/repo/manifest.json"
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{manifest_path} is not a valid JSON file.")

    assert isinstance(manifest, list), "Manifest should be a JSON array."
    assert len(manifest) == 2, f"Manifest should contain exactly 2 valid artifacts, found {len(manifest)}."

    incoming_dir = "/home/user/incoming"
    valid_files = {
        "alpha-tool.tar.gz": {"name": "alpha-tool", "version": "1.0.0", "type": "binary", "status": "release"},
        "beta-tool.zip": {"name": "beta-tool", "version": "2.1.0", "type": "binary", "status": "release"}
    }

    manifest_dict = {item.get("name"): item for item in manifest}

    for filename, expected_metadata in valid_files.items():
        filepath = os.path.join(incoming_dir, filename)
        assert os.path.isfile(filepath), f"Original file {filepath} is missing."

        file_hash = get_sha256(filepath)
        shard_dir = file_hash[:2]
        ext = ".tar.gz" if filename.endswith(".tar.gz") else ".zip"

        repo_filepath = os.path.join("/home/user/repo/artifacts", shard_dir, f"{file_hash}{ext}")
        assert os.path.isfile(repo_filepath), f"Artifact not found at expected sharded path: {repo_filepath}"

        repo_file_hash = get_sha256(repo_filepath)
        assert repo_file_hash == file_hash, f"Hash mismatch for {repo_filepath}"

        tool_name = expected_metadata["name"]
        assert tool_name in manifest_dict, f"{tool_name} is missing from the manifest."

        manifest_item = manifest_dict[tool_name]
        assert manifest_item.get("sha256") == file_hash, f"Manifest sha256 for {tool_name} does not match."
        assert manifest_item.get("type") == "binary", f"Manifest type for {tool_name} is incorrect."
        assert manifest_item.get("status") == "release", f"Manifest status for {tool_name} is incorrect."

def test_invalid_artifacts_not_in_repo():
    incoming_dir = "/home/user/incoming"
    invalid_files = ["gamma-source.tar.gz", "delta-tool.zip"]

    for filename in invalid_files:
        filepath = os.path.join(incoming_dir, filename)
        if os.path.isfile(filepath):
            file_hash = get_sha256(filepath)
            shard_dir = file_hash[:2]
            ext = ".tar.gz" if filename.endswith(".tar.gz") else ".zip"
            repo_filepath = os.path.join("/home/user/repo/artifacts", shard_dir, f"{file_hash}{ext}")
            assert not os.path.isfile(repo_filepath), f"Invalid artifact {filename} should not be in the repository."