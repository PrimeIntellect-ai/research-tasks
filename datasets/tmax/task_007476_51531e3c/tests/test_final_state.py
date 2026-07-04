# test_final_state.py

import os
import json
import pytest

PIPELINE_DIR = "/home/user/pipeline"
REPORT_PATH = os.path.join(PIPELINE_DIR, "build_report.json")

def test_build_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Expected output file {REPORT_PATH} was not found. Did the build script run successfully?"

def test_build_report_valid_json():
    try:
        with open(REPORT_PATH, 'r') as f:
            json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {REPORT_PATH} is not valid JSON.")
    except Exception as e:
        pytest.fail(f"Could not read {REPORT_PATH}: {e}")

def test_build_report_dependencies():
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    assert "dependencies" in data, "The 'dependencies' key is missing from the build report."

    deps = data["dependencies"]
    assert isinstance(deps, list), "'dependencies' should be a list."

    expected_deps = {"app", "core", "ui", "api", "utils", "frontend_lib", "backend_url"}
    actual_deps = set(deps)

    assert len(deps) == len(actual_deps), "There are duplicate dependencies in the report. The resolver might still have a bug."
    assert actual_deps == expected_deps, f"Dependencies mismatch. Expected {expected_deps}, but got {actual_deps}."

def test_build_report_owners():
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    assert "owners" in data, "The 'owners' key is missing from the build report."
    owners = data["owners"]

    assert isinstance(owners, dict), "'owners' should be a dictionary."

    assert owners.get("core") == "bob", "The owner for 'core' is incorrect. It should be the active owner ('bob')."
    assert owners.get("api") == "diana", "The owner for 'api' is incorrect. It should be the active owner ('diana')."
    assert owners.get("backend_url") == "heidi", "The owner for 'backend_url' is incorrect. It should be 'heidi'."