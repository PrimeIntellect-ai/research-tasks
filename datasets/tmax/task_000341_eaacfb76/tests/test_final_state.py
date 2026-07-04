# test_final_state.py

import os
import json
import pytest

REPO_DIR = "/home/user/repo"
MANIFEST_PATH = os.path.join(REPO_DIR, "manifest.json")

def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"The repository directory {REPO_DIR} was not created."

def test_curated_archives_exist():
    expected_files = [
        "arm64/alphatools-2.1.tar.gz",
        "x86_64/gammacore-3.0.1.zip"
    ]
    for rel_path in expected_files:
        full_path = os.path.join(REPO_DIR, rel_path)
        assert os.path.isfile(full_path), f"Expected curated artifact {full_path} is missing."

def test_ignored_artifacts_not_present():
    # BetaApp was 'testing' so it should not be in the repo
    # Check if any betaapp files exist in the repo
    for root, dirs, files in os.walk(REPO_DIR):
        for file in files:
            assert "beta" not in file.lower(), f"Artifact {file} should have been ignored (status was testing)."

def test_manifest_json():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} is missing."

    with open(MANIFEST_PATH, 'r') as f:
        try:
            manifest_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {MANIFEST_PATH} is not valid JSON.")

    assert isinstance(manifest_data, list), "Manifest JSON root should be a list."
    assert len(manifest_data) == 2, f"Manifest should contain exactly 2 items, found {len(manifest_data)}."

    expected_items = [
        {
            "name": "alphatools",
            "version": "2.1",
            "arch": "arm64",
            "build_id": "alpha-992",
            "file": "alphatools-2.1.tar.gz"
        },
        {
            "name": "gammacore",
            "version": "3.0.1",
            "arch": "x86_64",
            "build_id": "gamma-777",
            "file": "gammacore-3.0.1.zip"
        }
    ]

    for expected in expected_items:
        found = False
        for item in manifest_data:
            if item.get("name") == expected["name"]:
                found = True
                assert item.get("version") == expected["version"], f"Version mismatch for {expected['name']}"
                assert item.get("arch") == expected["arch"], f"Arch mismatch for {expected['name']}"
                assert item.get("build_id") == expected["build_id"], f"Build ID mismatch for {expected['name']}"
                assert item.get("file") == expected["file"], f"File mismatch for {expected['name']}"
                break
        assert found, f"Expected artifact {expected['name']} not found in manifest.json."