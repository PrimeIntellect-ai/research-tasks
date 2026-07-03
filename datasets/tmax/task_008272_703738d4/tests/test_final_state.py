# test_final_state.py

import os
import json
import pytest

PROJECT_DIR = "/home/user/auth_project"
REQUIREMENTS_FILE = os.path.join(PROJECT_DIR, "requirements.txt")
SHARED_LIB = os.path.join(PROJECT_DIR, "lib/libccrypto.so")
TEST_RESULTS_FILE = os.path.join(PROJECT_DIR, "test_results.json")

def test_requirements_modified():
    assert os.path.isfile(REQUIREMENTS_FILE), f"Requirements file is missing: {REQUIREMENTS_FILE}"
    with open(REQUIREMENTS_FILE, "r") as f:
        content = f.read()

    # Check that the original conflicting versions are not both present exactly as before
    conflict_present = "Flask==2.0.0" in content and "Werkzeug==3.0.0" in content
    assert not conflict_present, "requirements.txt still contains the conflicting Flask==2.0.0 and Werkzeug==3.0.0 versions."

def test_shared_library_exists():
    assert os.path.isfile(SHARED_LIB), f"Shared library is missing: {SHARED_LIB}"
    # Check if it's an ELF file
    with open(SHARED_LIB, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File {SHARED_LIB} is not a valid ELF shared object."

def test_python_scripts_exist():
    scripts = ["build_polyglot.py", "app.py", "test_e2e.py"]
    for script in scripts:
        script_path = os.path.join(PROJECT_DIR, script)
        assert os.path.isfile(script_path), f"Required script is missing: {script_path}"

def test_results_json():
    assert os.path.isfile(TEST_RESULTS_FILE), f"Test results file is missing: {TEST_RESULTS_FILE}"

    with open(TEST_RESULTS_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {TEST_RESULTS_FILE} does not contain valid JSON.")

    assert "hash" in data, "JSON result is missing the 'hash' key."
    expected_hash = "SECURE_test_password_123"
    assert data["hash"] == expected_hash, f"Expected hash '{expected_hash}', but got '{data['hash']}'"