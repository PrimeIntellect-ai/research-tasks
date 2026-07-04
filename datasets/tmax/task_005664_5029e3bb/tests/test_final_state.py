# test_final_state.py
import os
import json
import hashlib
import pytest

def test_script_exists_and_contains_requirements():
    """Test that the script exists and contains required modules."""
    script_path = '/home/user/process_docs.py'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    with open(script_path, 'r') as f:
        content = f.read()
    assert 'multiprocessing' in content, "Script does not use multiprocessing."
    assert 'fcntl' in content and 'flock' in content, "Script does not use fcntl.flock."

def test_processed_docs_files_and_line_counts():
    """Test that the processed_docs directory contains the correct files with correct line counts."""
    processed_dir = '/home/user/processed_docs'
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist."

    expected_files = {
        'intro.md': 30,
        'api_reference.md': 50,
        'advanced_guide_part1.md': 50,
        'advanced_guide_part2.md': 50,
        'advanced_guide_part3.md': 25
    }

    actual_files = os.listdir(processed_dir)
    assert set(actual_files) == set(expected_files.keys()), f"Files in {processed_dir} do not match expected files."

    for filename, expected_lines in expected_files.items():
        filepath = os.path.join(processed_dir, filename)
        with open(filepath, 'r') as f:
            lines = f.readlines()
        assert len(lines) == expected_lines, f"File {filename} has {len(lines)} lines, expected {expected_lines}."

def test_manifest_content():
    """Test that manifest.jsonl contains the correct JSON records."""
    manifest_path = '/home/user/manifest.jsonl'
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} does not exist."

    expected_records = [
        {"original": "intro.md", "chunks": ["intro.md"]},
        {"original": "api_reference.md", "chunks": ["api_reference.md"]},
        {"original": "advanced_guide.md", "chunks": ["advanced_guide_part1.md", "advanced_guide_part2.md", "advanced_guide_part3.md"]}
    ]

    actual_records = []
    with open(manifest_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                actual_records.append(json.loads(line))

    assert len(actual_records) == len(expected_records), "Manifest does not contain the expected number of records."

    # Sort both lists of dicts by 'original' key to compare
    expected_records.sort(key=lambda x: x['original'])
    actual_records.sort(key=lambda x: x['original'])

    assert actual_records == expected_records, "Manifest JSON records do not match expected records."

def test_manifest_checksum():
    """Test that manifest_checksum.txt contains the correct SHA256 checksum."""
    manifest_path = '/home/user/manifest.jsonl'
    checksum_path = '/home/user/manifest_checksum.txt'

    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} does not exist."
    assert os.path.exists(checksum_path), f"Checksum file {checksum_path} does not exist."

    # Calculate actual sha256
    sha256 = hashlib.sha256()
    with open(manifest_path, 'rb') as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    actual_hash = sha256.hexdigest()

    with open(checksum_path, 'r') as f:
        checksum_content = f.read().strip()

    assert checksum_content.startswith(actual_hash), "Checksum in manifest_checksum.txt does not match the actual SHA256 of manifest.jsonl."
    assert 'manifest.jsonl' in checksum_content, "Checksum file does not contain the filename 'manifest.jsonl'."