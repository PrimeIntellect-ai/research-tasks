# test_final_state.py

import os
import json
import hashlib

def test_skipped_log_exists_and_correct():
    skipped_log_path = '/home/user/skipped.log'
    assert os.path.isfile(skipped_log_path), f"Skipped log file is missing at {skipped_log_path}"

    with open(skipped_log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 1, f"Expected exactly one skipped file, but found {len(lines)}"
    assert lines[0] == '../system_config.txt', f"Expected '../system_config.txt' to be skipped, got '{lines[0]}'"

def test_project_restore_files_exist_and_correct():
    restore_dir = '/home/user/project_restore'
    assert os.path.isdir(restore_dir), f"Restore directory missing at {restore_dir}"

    expected_files = {
        'README.md': b'Base v1',
        'src/app.py': b'print("Hello v2")',
        'src/utils.py': b'def foo(): pass',
        'docs/index.md': b'Docs'
    }

    for rel_path, expected_content in expected_files.items():
        full_path = os.path.join(restore_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected restored file missing: {full_path}"

        with open(full_path, 'rb') as f:
            content = f.read()

        assert content == expected_content, f"Content mismatch in {full_path}. Expected {expected_content}, got {content}"

def test_manifest_json_exists_and_correct():
    manifest_path = '/home/user/manifest.json'
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Manifest file at {manifest_path} is not valid JSON"

    expected_hashes = {
        'README.md': hashlib.sha256(b'Base v1').hexdigest(),
        'src/app.py': hashlib.sha256(b'print("Hello v2")').hexdigest(),
        'src/utils.py': hashlib.sha256(b'def foo(): pass').hexdigest(),
        'docs/index.md': hashlib.sha256(b'Docs').hexdigest()
    }

    assert isinstance(manifest, dict), "Manifest should be a JSON object (dictionary)"
    assert len(manifest) == len(expected_hashes), f"Expected {len(expected_hashes)} entries in manifest, got {len(manifest)}"

    for rel_path, expected_hash in expected_hashes.items():
        assert rel_path in manifest, f"Missing {rel_path} in manifest.json"
        assert manifest[rel_path] == expected_hash, f"Hash mismatch for {rel_path}. Expected {expected_hash}, got {manifest[rel_path]}"

def test_no_malicious_files_extracted():
    malicious_path = '/home/user/system_config.txt'
    assert not os.path.exists(malicious_path), f"Malicious file was extracted to {malicious_path}"

    malicious_path_2 = '/home/system_config.txt'
    assert not os.path.exists(malicious_path_2), f"Malicious file was extracted to {malicious_path_2}"