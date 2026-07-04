# test_final_state.py

import os
import json
import glob
import hashlib
import pytest

RESULT_JSON_PATH = "/home/user/result.json"
PACKAGE_DIR = "/home/user/my_package"
DIST_DIR = os.path.join(PACKAGE_DIR, "dist")
PYPROJECT_PATH = os.path.join(PACKAGE_DIR, "pyproject.toml")

def test_pyproject_toml_fixed():
    """Check if pyproject.toml was fixed with name and version."""
    assert os.path.isfile(PYPROJECT_PATH), f"{PYPROJECT_PATH} is missing."
    with open(PYPROJECT_PATH, "r") as f:
        content = f.read()
    assert "my_package" in content, "pyproject.toml is missing the package name 'my_package'."
    assert "0.1.0" in content, "pyproject.toml is missing the version '0.1.0'."

def test_package_built():
    """Check if the Python package was successfully built into a source distribution."""
    assert os.path.isdir(DIST_DIR), f"{DIST_DIR} directory is missing. Build may have failed."
    tar_files = glob.glob(os.path.join(DIST_DIR, "*.tar.gz"))
    assert len(tar_files) > 0, "No .tar.gz file found in the dist directory."

def test_result_json_exists_and_valid():
    """Check if result.json exists and contains strictly valid JSON."""
    assert os.path.isfile(RESULT_JSON_PATH), f"{RESULT_JSON_PATH} is missing."
    try:
        with open(RESULT_JSON_PATH, "r") as f:
            json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{RESULT_JSON_PATH} does not contain valid JSON.")

def test_result_json_content():
    """Check if result.json contains the correct values based on the task."""
    with open(RESULT_JSON_PATH, "r") as f:
        data = json.load(f)

    # Check job_id
    assert "job_id" in data, "result.json is missing 'job_id'."
    assert data["job_id"] == "job_9981", f"Expected job_id to be 'job_9981', got '{data['job_id']}'."

    # Check expected_checksum
    expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert "expected_checksum" in data, "result.json is missing 'expected_checksum'."
    assert data["expected_checksum"] == expected_hash, f"Expected expected_checksum to be '{expected_hash}', got '{data['expected_checksum']}'."

    # Compute actual checksum
    tar_files = glob.glob(os.path.join(DIST_DIR, "*.tar.gz"))
    assert len(tar_files) > 0, "Cannot compute actual checksum because no .tar.gz file exists."

    with open(tar_files[0], "rb") as f:
        file_bytes = f.read()
        computed_hash = hashlib.sha256(file_bytes).hexdigest()

    # Check actual_checksum
    assert "actual_checksum" in data, "result.json is missing 'actual_checksum'."
    assert data["actual_checksum"] == computed_hash, f"Expected actual_checksum to be '{computed_hash}', got '{data['actual_checksum']}'."

    # Check match boolean
    assert "match" in data, "result.json is missing 'match'."
    assert isinstance(data["match"], bool), "'match' in result.json must be a boolean."
    expected_match = (computed_hash == expected_hash)
    assert data["match"] == expected_match, f"Expected match to be {expected_match}, got {data['match']}."