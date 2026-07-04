# test_final_state.py

import os
import json
import pytest

REPORT_JSON = "/home/user/pipeline/report.json"
ORCHESTRATOR_PY = "/home/user/pipeline/orchestrator.py"

def test_orchestrator_exists():
    assert os.path.isfile(ORCHESTRATOR_PY), f"Expected script {ORCHESTRATOR_PY} does not exist."

def test_report_json_exists():
    assert os.path.isfile(REPORT_JSON), f"Expected output file {REPORT_JSON} does not exist."

def test_report_json_content():
    with open(REPORT_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_JSON} is not valid JSON.")

    assert "packages" in data, "Report JSON is missing the 'packages' top-level key."
    packages = data["packages"]

    expected_packages = {
        "libcore": {
            "version": "1.2.5",
            "compile_warnings": 2
        },
        "py-bindings": {
            "version": "1.0.1",
            "compile_warnings": 3
        },
        "rust-service": {
            "version": "3.1.0",
            "compile_warnings": 0
        }
    }

    for pkg, expected_info in expected_packages.items():
        assert pkg in packages, f"Package '{pkg}' is missing from the report."
        actual_info = packages[pkg]

        assert "version" in actual_info, f"Missing 'version' for package '{pkg}'."
        assert actual_info["version"] == expected_info["version"], \
            f"Expected version {expected_info['version']} for '{pkg}', but got {actual_info['version']}."

        assert "compile_warnings" in actual_info, f"Missing 'compile_warnings' for package '{pkg}'."
        assert actual_info["compile_warnings"] == expected_info["compile_warnings"], \
            f"Expected {expected_info['compile_warnings']} compile_warnings for '{pkg}', but got {actual_info['compile_warnings']}."

    # Check for extra packages
    for pkg in packages:
        assert pkg in expected_packages, f"Unexpected package '{pkg}' found in the report."