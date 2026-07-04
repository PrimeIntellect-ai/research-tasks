# test_final_state.py
import os
import subprocess
import hashlib
import pytest

def test_wal_classifier_exists():
    assert os.path.isfile("/home/user/wal_classifier.sh"), "/home/user/wal_classifier.sh does not exist."

def test_classifier_clean_corpus():
    clean_dir = "/app/verifier/clean/"
    assert os.path.isdir(clean_dir), f"Missing verifier clean dir: {clean_dir}"

    failed_files = []
    total_files = 0
    for root, _, files in os.walk(clean_dir):
        for file in files:
            filepath = os.path.join(root, file)
            total_files += 1
            result = subprocess.run(["bash", "/home/user/wal_classifier.sh", filepath], capture_output=True)
            if result.returncode != 0:
                failed_files.append(file)

    assert len(failed_files) == 0, f"{len(failed_files)} of {total_files} clean modified/rejected. Offending files: {', '.join(failed_files)}"

def test_classifier_evil_corpus():
    evil_dir = "/app/verifier/evil/"
    assert os.path.isdir(evil_dir), f"Missing verifier evil dir: {evil_dir}"

    bypassed_files = []
    total_files = 0
    for root, _, files in os.walk(evil_dir):
        for file in files:
            filepath = os.path.join(root, file)
            total_files += 1
            result = subprocess.run(["bash", "/home/user/wal_classifier.sh", filepath], capture_output=True)
            if result.returncode == 0:
                bypassed_files.append(file)

    assert len(bypassed_files) == 0, f"{len(bypassed_files)} of {total_files} evil bypassed. Offending files: {', '.join(bypassed_files)}"

def test_clean_manifest():
    manifest_path = "/home/user/clean_manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    with open(manifest_path, "r") as f:
        manifest_lines = f.read().strip().split('\n')

    manifest_dict = {}
    for line in manifest_lines:
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            checksum, path = parts
            manifest_dict[path.strip().lstrip('*')] = checksum.strip()

    clean_dir = "/app/corpus/clean/"
    actual_files = []
    for root, _, files in os.walk(clean_dir):
        for file in files:
            actual_files.append(os.path.join(root, file))

    assert len(actual_files) > 0, "No files found in /app/corpus/clean/"

    for filepath in actual_files:
        with open(filepath, "rb") as f:
            expected_hash = hashlib.sha256(f.read()).hexdigest()

        found = False
        for m_path, m_hash in manifest_dict.items():
            if m_path.endswith(os.path.basename(filepath)):
                assert m_hash == expected_hash, f"Checksum mismatch for {filepath}. Expected {expected_hash}, got {m_hash}."
                found = True
                break
        assert found, f"File {filepath} not found in manifest."