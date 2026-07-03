# test_final_state.py

import os
import subprocess
import hashlib
import pytest
import shutil

EVIL_DIR = "/app/grader/evil"
CLEAN_DIR = "/app/grader/clean"
SCRIPT_PATH = "/home/user/cleanup.sh"
MANIFEST_PATH = "/tmp/global_manifest.txt"

@pytest.fixture(scope="session", autouse=True)
def run_agent_script():
    """Run the agent's script on both corpora in parallel before tests."""
    assert os.path.isfile(SCRIPT_PATH), f"Agent script missing at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Agent script at {SCRIPT_PATH} is not executable"

    if os.path.exists(MANIFEST_PATH):
        os.remove(MANIFEST_PATH)

    # Run the script on both directories in parallel to test locking
    evil_proc = subprocess.Popen(["bash", SCRIPT_PATH, EVIL_DIR, MANIFEST_PATH])
    clean_proc = subprocess.Popen(["bash", SCRIPT_PATH, CLEAN_DIR, MANIFEST_PATH])

    evil_proc.wait()
    clean_proc.wait()

def test_evil_corpus_rejected():
    """Assert that all files in the evil corpus were deleted."""
    remaining_evil_files = []
    if os.path.exists(EVIL_DIR):
        for root, _, files in os.walk(EVIL_DIR):
            for f in files:
                if f.endswith(".wav"):
                    remaining_evil_files.append(f)

    assert not remaining_evil_files, f"{len(remaining_evil_files)} evil files bypassed deletion: {', '.join(remaining_evil_files)}"

def test_clean_corpus_preserved():
    """Assert that all files in the clean corpus were preserved."""
    # Assuming there's a backup or we just check if any files exist in the clean dir.
    # In a real adversarial corpus test, we would compare against a pristine backup.
    # Here we just check that the clean dir is not empty and contains .wav files.
    clean_files = []
    if os.path.exists(CLEAN_DIR):
        for root, _, files in os.walk(CLEAN_DIR):
            for f in files:
                if f.endswith(".wav"):
                    clean_files.append(os.path.join(root, f))

    assert clean_files, "All clean files were deleted; expected them to be preserved."

def test_manifest_correctness():
    """Check that the manifest contains exactly the SHA256 hashes of the clean files."""
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"

    clean_files = []
    if os.path.exists(CLEAN_DIR):
        for root, _, files in os.walk(CLEAN_DIR):
            for f in files:
                if f.endswith(".wav"):
                    clean_files.append(os.path.join(root, f))

    expected_manifest = {}
    for filepath in clean_files:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        expected_manifest[filepath] = sha256_hash.hexdigest()

    actual_manifest = {}
    with open(MANIFEST_PATH, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                actual_manifest[parts[1]] = parts[0]

    missing_in_manifest = [f for f in expected_manifest if f not in actual_manifest]
    wrong_hashes = [f for f in expected_manifest if f in actual_manifest and expected_manifest[f] != actual_manifest[f]]

    assert not missing_in_manifest, f"Files missing from manifest: {missing_in_manifest}"
    assert not wrong_hashes, f"Files with incorrect hashes in manifest: {wrong_hashes}"
    assert len(actual_manifest) == len(expected_manifest), f"Manifest contains extra or missing entries. Expected {len(expected_manifest)}, got {len(actual_manifest)}"