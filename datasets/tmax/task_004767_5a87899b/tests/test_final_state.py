# test_final_state.py

import os
import json
import pytest

WORKSPACE_DIR = "/home/user/workspace"
VALID_PAYLOADS_FILE = os.path.join(WORKSPACE_DIR, "valid_payloads.json")
LIBSECCHECK_SO = os.path.join(WORKSPACE_DIR, "libseccheck.so")
DEPLOY_PREP_PY = os.path.join(WORKSPACE_DIR, "deploy_prep.py")

def test_libseccheck_so_exists():
    assert os.path.isfile(LIBSECCHECK_SO), f"Compiled shared library {LIBSECCHECK_SO} is missing."

def test_deploy_prep_script_exists():
    assert os.path.isfile(DEPLOY_PREP_PY), f"Python script {DEPLOY_PREP_PY} is missing."

def test_valid_payloads_json_exists():
    assert os.path.isfile(VALID_PAYLOADS_FILE), f"Output file {VALID_PAYLOADS_FILE} is missing. Did you execute the script?"

def test_valid_payloads_content():
    assert os.path.isfile(VALID_PAYLOADS_FILE), f"Cannot test content, {VALID_PAYLOADS_FILE} is missing."

    with open(VALID_PAYLOADS_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {VALID_PAYLOADS_FILE} does not contain valid JSON.")

    expected_ids = ["config_alpha", "config_delta"]

    assert isinstance(data, list), f"Expected a JSON array in {VALID_PAYLOADS_FILE}, but got {type(data).__name__}."
    assert data == expected_ids, f"Expected {expected_ids}, but got {data}. Ensure the C function's logic is correctly applied to the payloads."