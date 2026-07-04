# test_final_state.py

import os
import subprocess
import tarfile
import json
import hashlib
import shutil
import pytest

SCRIPT_PATH = "/home/user/curate_audio.sh"
EVIL_DIR = "/app/audio_eval/evil"
CLEAN_DIR = "/app/audio_eval/clean"
COMBINED_DIR = "/app/audio_eval/combined_test_dir"
OUTPUT_TAR = "/tmp/output.tar.gz"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_curation_pipeline():
    # Setup combined directory
    if os.path.exists(COMBINED_DIR):
        shutil.rmtree(COMBINED_DIR)
    os.makedirs(COMBINED_DIR)

    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.wav')]
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.wav')]

    for f in evil_files:
        shutil.copy(os.path.join(EVIL_DIR, f), os.path.join(COMBINED_DIR, f))
    for f in clean_files:
        shutil.copy(os.path.join(CLEAN_DIR, f), os.path.join(COMBINED_DIR, f))

    if os.path.exists(OUTPUT_TAR):
        os.remove(OUTPUT_TAR)

    # Run the script
    result = subprocess.run([SCRIPT_PATH, COMBINED_DIR, OUTPUT_TAR], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    assert os.path.exists(OUTPUT_TAR), f"Output archive {OUTPUT_TAR} was not created"

    # Extract and verify
    extract_dir = "/tmp/extracted_output"
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)

    with tarfile.open(OUTPUT_TAR, "r:gz") as tar:
        tar.extractall(path=extract_dir)

    manifest_path = os.path.join(extract_dir, "manifest.json")
    assert os.path.exists(manifest_path), "manifest.json not found in the archive"

    with open(manifest_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("manifest.json is not valid JSON")

    assert "files" in manifest, "manifest.json does not contain 'files' key"
    manifest_files = {item.get("filename"): item for item in manifest.get("files", [])}

    # Check evil files are rejected
    evil_bypassed = []
    for f in evil_files:
        if f in manifest_files or os.path.exists(os.path.join(extract_dir, f)):
            evil_bypassed.append(f)

    # Check clean files are preserved
    clean_modified = []
    for f in clean_files:
        if f not in manifest_files or not os.path.exists(os.path.join(extract_dir, f)):
            clean_modified.append(f)
            continue

        # Verify SHA256 and size
        original_path = os.path.join(CLEAN_DIR, f)
        original_size = os.path.getsize(original_path)
        with open(original_path, "rb") as orig_f:
            original_sha256 = hashlib.sha256(orig_f.read()).hexdigest()

        manifest_item = manifest_files[f]
        if manifest_item.get("size") != original_size:
            clean_modified.append(f"{f} (wrong size)")
        if manifest_item.get("sha256") != original_sha256:
            clean_modified.append(f"{f} (wrong sha256)")

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/missing: {', '.join(clean_modified)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))