# test_final_state.py

import os
import json
import subprocess
import pytest

PIPELINE_DIR = "/home/user/artifact_pipeline"

def test_makefile_exists_and_runs():
    makefile_path = os.path.join(PIPELINE_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile is missing in {PIPELINE_DIR}"

    # Run make ci-run to ensure it executes successfully
    result = subprocess.run(["make", "ci-run"], cwd=PIPELINE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"'make ci-run' failed with exit code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

def test_artifacts_json_is_patched():
    artifacts_path = os.path.join(PIPELINE_DIR, "artifacts.json")
    assert os.path.isfile(artifacts_path), f"File {artifacts_path} is missing."

    with open(artifacts_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {artifacts_path} is not valid JSON.")

    # Find build-102 and verify it was patched
    build_102 = next((item for item in data if item.get("id") == "build-102"), None)
    assert build_102 is not None, "build-102 is missing from artifacts.json"

    assert build_102.get("coverage") == 0.95, "artifacts.json was not properly patched: coverage for build-102 should be 0.95"
    assert build_102.get("complexity") == 3, "artifacts.json was not properly patched: complexity for build-102 should be 3"

def test_approved_txt_content():
    approved_path = os.path.join(PIPELINE_DIR, "approved.txt")
    assert os.path.isfile(approved_path), f"{approved_path} does not exist. Ensure scorer.py generates it."

    with open(approved_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["build-101", "build-102"]
    assert set(lines) == set(expected), f"approved.txt does not contain the expected artifact IDs. Expected {expected}, got {lines}"
    assert len(lines) == len(expected), "approved.txt contains duplicate or extra lines."