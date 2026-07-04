# test_final_state.py

import os
import json
import pytest

INVESTIGATION_JSON = "/home/user/investigation.json"
VENV_DIR = "/home/user/service/venv"

def test_investigation_json_exists():
    assert os.path.isfile(INVESTIGATION_JSON), f"File {INVESTIGATION_JSON} does not exist."

def test_investigation_json_content():
    with open(INVESTIGATION_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{INVESTIGATION_JSON} is not a valid JSON file.")

    assert "fixed_markup_safe_version" in data, "Missing 'fixed_markup_safe_version' in JSON."
    assert "leaked_secret_key" in data, "Missing 'leaked_secret_key' in JSON."
    assert "deadlock_payload" in data, "Missing 'deadlock_payload' in JSON."

    assert data["leaked_secret_key"] == "SECRET_KEY_BEGIN_ZGVhZGxlYWtfczNjcjN0X2tleV8yMDIz_END", \
        "Incorrect leaked_secret_key extracted from the memory dump."

    assert data["deadlock_payload"] == "HANG_ME", \
        "Incorrect deadlock_payload discovered."

    version = data["fixed_markup_safe_version"]
    assert isinstance(version, str), "fixed_markup_safe_version must be a string."
    assert version.startswith("1."), f"fixed_markup_safe_version should be a 1.x version to resolve the conflict, got {version}."

def test_venv_exists():
    python_bin = os.path.join(VENV_DIR, "bin", "python")
    python3_bin = os.path.join(VENV_DIR, "bin", "python3")
    assert os.path.isfile(python_bin) or os.path.isfile(python3_bin), \
        f"Virtual environment not found or missing python binary at {VENV_DIR}."