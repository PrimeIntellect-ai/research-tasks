# test_final_state.py

import os
import stat
import json
import hashlib
import pytest

def get_expected_vulnerabilities():
    known_hashes_path = "/home/user/known_hashes.txt"
    system_mock_dir = "/home/user/system_mock"

    if not os.path.isfile(known_hashes_path):
        return []

    # Read known hashes
    known_hashes = {}
    with open(known_hashes_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                file_hash = parts[0]
                file_path = " ".join(parts[1:])
                known_hashes[file_path] = file_hash

    expected_results = []

    # Walk the directory
    for root, _, files in os.walk(system_mock_dir):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Calculate SHA-256
            sha256_hash = hashlib.sha256()
            try:
                with open(filepath, "rb") as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
                calculated_hash = sha256_hash.hexdigest()
            except Exception:
                continue

            # Verify hash
            if filepath not in known_hashes or known_hashes[filepath] != calculated_hash:
                continue

            # Check permissions
            try:
                st = os.stat(filepath)
                mode = st.st_mode
            except Exception:
                continue

            is_suid = bool(mode & stat.S_ISUID)
            is_world_writable = bool(mode & stat.S_IWOTH)

            if is_suid:
                expected_results.append({
                    "file": filepath,
                    "vulnerability": "SUID"
                })
            elif is_world_writable:
                expected_results.append({
                    "file": filepath,
                    "vulnerability": "World-Writable"
                })

    # Sort alphabetically by file path
    expected_results.sort(key=lambda x: x["file"])
    return expected_results

def test_evasion_log_exists():
    log_path = "/home/user/evasion_log.json"
    assert os.path.isfile(log_path), f"The output file {log_path} does not exist."

def test_evasion_log_contents():
    log_path = "/home/user/evasion_log.json"
    assert os.path.isfile(log_path), f"The output file {log_path} does not exist."

    with open(log_path, 'r') as f:
        try:
            actual_log = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {log_path} does not contain valid JSON.")

    expected_log = get_expected_vulnerabilities()

    assert isinstance(actual_log, list), "The JSON output must be an array."
    assert len(actual_log) == len(expected_log), f"Expected {len(expected_log)} vulnerabilities, but found {len(actual_log)}."

    for i, (actual, expected) in enumerate(zip(actual_log, expected_log)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        assert "file" in actual, f"Item at index {i} is missing the 'file' key."
        assert "vulnerability" in actual, f"Item at index {i} is missing the 'vulnerability' key."

        assert actual["file"] == expected["file"], f"Expected file path '{expected['file']}' at index {i}, got '{actual['file']}'."
        assert actual["vulnerability"] == expected["vulnerability"], f"Expected vulnerability '{expected['vulnerability']}' for file '{actual['file']}', got '{actual['vulnerability']}'."

def test_rust_project_exists():
    cargo_toml = "/home/user/payload/Cargo.toml"
    assert os.path.isfile(cargo_toml), "Rust project was not created at /home/user/payload (Cargo.toml missing)."