# test_final_state.py

import os
import json
import hashlib
import pytest
import ast

def get_expected_data():
    base_dir = "/home/user/artifacts"
    expected = []

    # We will compute the expected hashes and data dynamically based on the files created in setup.
    # The setup created app_v1, app_v2, helper.
    files_info = [
        ("v1.0/app_v1.bin", "v1.0/app_v1.json"),
        ("v2.0/app_v2.bin", "v2.0/app_v2.json"),
        ("v2.0/sub_module/helper.bin", "v2.0/sub_module/helper.json")
    ]

    for bin_rel, json_rel in files_info:
        bin_path = os.path.join(base_dir, bin_rel)
        json_path = os.path.join(base_dir, json_rel)

        with open(bin_path, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()

        with open(json_path, "r") as f:
            meta = json.load(f)

        expected.append({
            "artifact_path": bin_path,
            "sha256": sha256,
            "name": meta["name"],
            "version": meta["version"]
        })

    return expected

def test_indexer_script_exists_and_uses_fcntl():
    script_path = "/home/user/indexer.py"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    assert "fcntl.flock" in content, "The script must use fcntl.flock to ensure concurrent-safe manifest writing."
    assert "LOCK_EX" in content, "The script must use LOCK_EX for exclusive locking."

def test_skipped_links_log():
    log_path = "/home/user/skipped_links.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 1, "The log file should contain at least one skipped symlink."

    # The loop link is /home/user/artifacts/v2.0/legacy_loop
    # Depending on traversal order, it could be the direct one or via latest.
    valid_loops = [
        "/home/user/artifacts/v2.0/legacy_loop",
        "/home/user/artifacts/latest/legacy_loop"
    ]

    found_loop = any(loop in lines for loop in valid_loops)
    assert found_loop, f"The log file must contain the skipped infinite loop symlink. Found: {lines}"

def test_manifest_json():
    manifest_path = "/home/user/manifest.json"
    assert os.path.isfile(manifest_path), f"Manifest file missing: {manifest_path}"

    with open(manifest_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not a valid JSON file.")

    assert isinstance(data, list), "Manifest must be a JSON array."

    expected_data = get_expected_data()

    # Create a lookup for expected items by their realpath to handle symlink paths if they were traversed
    expected_lookup = {os.path.realpath(item["artifact_path"]): item for item in expected_data}

    # Verify each entry in the manifest
    for entry in data:
        assert "artifact_path" in entry, "Missing 'artifact_path' in manifest entry."
        assert "sha256" in entry, "Missing 'sha256' in manifest entry."
        assert "name" in entry, "Missing 'name' in manifest entry."
        assert "version" in entry, "Missing 'version' in manifest entry."

        real_path = os.path.realpath(entry["artifact_path"])
        assert real_path in expected_lookup, f"Unexpected artifact path in manifest: {entry['artifact_path']}"

        expected_item = expected_lookup[real_path]
        assert entry["sha256"] == expected_item["sha256"], f"Incorrect SHA256 for {entry['artifact_path']}"
        assert entry["name"] == expected_item["name"], f"Incorrect name for {entry['artifact_path']}"
        assert entry["version"] == expected_item["version"], f"Incorrect version for {entry['artifact_path']}"

    # Ensure all expected real binaries are represented at least once
    found_real_paths = {os.path.realpath(entry["artifact_path"]) for entry in data}
    assert found_real_paths == set(expected_lookup.keys()), "Not all expected artifacts are present in the manifest."