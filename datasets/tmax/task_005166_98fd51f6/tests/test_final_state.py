# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_deployment.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
DEPLOYMENTS_DIR = "/home/user/deployments"
IMAGES_DIR = "/home/user/images"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK) or os.access(SCRIPT_PATH, os.R_OK), f"Script at {SCRIPT_PATH} is not readable/executable"

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            capture_output=True,
            text=True
        )
        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            bypassed.append(filename)

    assert not bypassed, f"{len(bypassed)} out of {len(evil_files)} evil files bypassed validation: {bypassed}"

def test_clean_corpus_accepted():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed = []
    side_effect_failures = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)

        with open(filepath, 'r') as f:
            config = json.load(f)

        service_name = config.get("service_name")
        vm_image_path = config.get("vm_image_path")

        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            capture_output=True,
            text=True
        )

        if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
            failed.append(filename)
            continue

        # Verify side effects
        service_dir = os.path.join(DEPLOYMENTS_DIR, service_name)
        symlink_path = os.path.join(service_dir, "latest")
        expected_target = os.path.normpath(os.path.join(IMAGES_DIR, vm_image_path))

        if not os.path.isdir(service_dir):
            side_effect_failures.append(f"{filename}: directory {service_dir} missing")
            continue

        if not os.path.islink(symlink_path):
            side_effect_failures.append(f"{filename}: symlink {symlink_path} missing")
            continue

        actual_target = os.readlink(symlink_path)
        if actual_target != expected_target:
            side_effect_failures.append(f"{filename}: symlink points to {actual_target}, expected {expected_target}")

    assert not failed, f"{len(failed)} out of {len(clean_files)} clean files were incorrectly rejected: {failed}"
    assert not side_effect_failures, f"Side effect validation failed for clean files: {side_effect_failures}"