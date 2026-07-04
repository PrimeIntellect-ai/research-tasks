# test_final_state.py
import os
import json
import tarfile
import hashlib
import pytest

def test_go_script_exists():
    assert os.path.isfile("/home/user/process_configs.go"), "Go script /home/user/process_configs.go does not exist."

def test_processed_json_files():
    expected_files = {
        "frontend_v1.0.4.json": {"service": "frontend", "version": "1.0.4", "port": 3000, "features": ["auth", "dashboard"]},
        "database_v13.2.json": {"service": "database", "version": "13.2", "max_connections": 100},
        "redis_cache_v6.2.0.json": {"service": "redis_cache", "version": "6.2.0", "max_memory": "4gb"}
    }

    processed_dir = "/home/user/processed_configs"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist."

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(processed_dir, filename)
        assert os.path.isfile(filepath), f"Expected processed file {filepath} is missing."

        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"File {filepath} is not valid JSON.")

        assert "debug_token" not in data, f"debug_token was not removed from {filename}."

        for key, val in expected_content.items():
            assert key in data, f"Key '{key}' is missing in {filename}."
            assert data[key] == val, f"Value for '{key}' in {filename} is incorrect."

def test_manifest_checksums():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    processed_dir = "/home/user/processed_configs"

    # Read manifest
    with open(manifest_path, 'r') as f:
        manifest_lines = f.read().strip().splitlines()

    manifest_hashes = {}
    for line in manifest_lines:
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            manifest_hashes[parts[1].strip()] = parts[0].strip()

    expected_files = ["frontend_v1.0.4.json", "database_v13.2.json", "redis_cache_v6.2.0.json"]
    for filename in expected_files:
        filepath = os.path.join(processed_dir, filename)
        assert os.path.isfile(filepath), f"Missing file {filepath} for checksum validation."

        with open(filepath, 'rb') as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()

        # The manifest might have filenames with or without path prefix depending on how it was run,
        # but the instructions said "from inside the processed_configs directory", so it should just be the filename
        # or prefixed with './'
        found = False
        for manifest_file, manifest_hash in manifest_hashes.items():
            if os.path.basename(manifest_file) == filename:
                assert manifest_hash == actual_hash, f"Checksum mismatch for {filename} in manifest."
                found = True
                break
        assert found, f"File {filename} not found in manifest.txt."

def test_final_archive():
    archive_path = "/home/user/final_configs.tar.gz"
    assert os.path.isfile(archive_path), f"Final archive {archive_path} is missing."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()

            # Check for manifest
            assert any(os.path.basename(n) == "manifest.txt" for n in names), "manifest.txt missing from final archive."

            # Check for processed configs
            expected_files = ["frontend_v1.0.4.json", "database_v13.2.json", "redis_cache_v6.2.0.json"]
            for expected_file in expected_files:
                assert any(os.path.basename(n) == expected_file for n in names), f"{expected_file} missing from final archive."

    except tarfile.ReadError:
        pytest.fail(f"Failed to read {archive_path}. It may not be a valid tar.gz file.")