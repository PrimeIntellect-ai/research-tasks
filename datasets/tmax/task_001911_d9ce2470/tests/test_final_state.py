# test_final_state.py

import os
import json
import hashlib
import tarfile
import pytest

PROCESSED_DIR = "/home/user/processed_data"
ALPHA_JSONL = os.path.join(PROCESSED_DIR, "dataset_alpha.jsonl")
BETA_JSONL = os.path.join(PROCESSED_DIR, "dataset_beta.jsonl")
MANIFEST = os.path.join(PROCESSED_DIR, "manifest.txt")
TAR_ARCHIVE = "/home/user/final_dataset.tar.gz"

def test_processed_alpha_jsonl():
    assert os.path.isfile(ALPHA_JSONL), f"File {ALPHA_JSONL} is missing."

    try:
        with open(ALPHA_JSONL, "r", encoding="utf-8") as f:
            lines = f.read().strip().split('\n')
    except UnicodeDecodeError:
        pytest.fail(f"{ALPHA_JSONL} is not properly encoded in UTF-8.")

    assert len(lines) == 2, f"Expected 2 lines in {ALPHA_JSONL}, found {len(lines)}."

    try:
        data = [json.loads(line) for line in lines]
    except json.JSONDecodeError:
        pytest.fail(f"{ALPHA_JSONL} contains invalid JSON.")

    expected_data = [
        {"id": "1", "name": "café", "measure": "12.5"},
        {"id": "2", "name": "jalapeño", "measure": "8.4"}
    ]

    assert data == expected_data, f"Content of {ALPHA_JSONL} does not match expected output."

def test_processed_beta_jsonl():
    assert os.path.isfile(BETA_JSONL), f"File {BETA_JSONL} is missing."

    try:
        with open(BETA_JSONL, "r", encoding="utf-8") as f:
            lines = f.read().strip().split('\n')
    except UnicodeDecodeError:
        pytest.fail(f"{BETA_JSONL} is not properly encoded in UTF-8.")

    assert len(lines) == 2, f"Expected 2 lines in {BETA_JSONL}, found {len(lines)}."

    try:
        data = [json.loads(line) for line in lines]
    except json.JSONDecodeError:
        pytest.fail(f"{BETA_JSONL} contains invalid JSON.")

    expected_data = [
        {"id": 3, "name": "résumé", "measure": 4.1},
        {"id": 4, "name": "piñata", "measure": 9.9}
    ]

    assert data == expected_data, f"Content of {BETA_JSONL} does not match expected output."

def test_manifest_checksums():
    assert os.path.isfile(MANIFEST), f"Manifest file {MANIFEST} is missing."

    with open(MANIFEST, "r", encoding="utf-8") as f:
        manifest_content = f.read().strip()

    def get_sha256(filepath):
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            h.update(f.read())
        return h.hexdigest()

    alpha_hash = get_sha256(ALPHA_JSONL)
    beta_hash = get_sha256(BETA_JSONL)

    # Allow single or double spaces between hash and filename
    assert f"{alpha_hash}  dataset_alpha.jsonl" in manifest_content or f"{alpha_hash} dataset_alpha.jsonl" in manifest_content, \
        f"Manifest does not contain correct SHA-256 hash for dataset_alpha.jsonl."

    assert f"{beta_hash}  dataset_beta.jsonl" in manifest_content or f"{beta_hash} dataset_beta.jsonl" in manifest_content, \
        f"Manifest does not contain correct SHA-256 hash for dataset_beta.jsonl."

def test_tar_archive():
    assert os.path.isfile(TAR_ARCHIVE), f"Archive {TAR_ARCHIVE} is missing."

    try:
        with tarfile.open(TAR_ARCHIVE, "r:gz") as tar:
            names = tar.getnames()

            # Check for expected files inside processed_data directory
            expected_files = [
                "processed_data/dataset_alpha.jsonl",
                "processed_data/dataset_beta.jsonl",
                "processed_data/manifest.txt"
            ]

            for expected in expected_files:
                # Account for potential './' prefix in tarball paths
                assert expected in names or f"./{expected}" in names, \
                    f"File {expected} is missing from the archive."

    except tarfile.ReadError:
        pytest.fail(f"File {TAR_ARCHIVE} is not a valid gzip-compressed tar archive.")