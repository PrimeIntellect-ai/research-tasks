# test_final_state.py

import os
import json
import pytest

FINAL_REPORT_PATH = "/home/user/final_report.json"
MONOREPO_PATH = "/home/user/monorepo"

def test_final_report_exists():
    assert os.path.isfile(FINAL_REPORT_PATH), f"The final report file {FINAL_REPORT_PATH} does not exist."

def test_final_report_content():
    assert os.path.isfile(FINAL_REPORT_PATH), f"Cannot check content, {FINAL_REPORT_PATH} is missing."

    with open(FINAL_REPORT_PATH, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {FINAL_REPORT_PATH} does not contain valid JSON.")

    expected_data = {
        "core_cpp": {
            "module": "core_cpp",
            "status": "compiled",
            "value": 42
        },
        "utils_py": {
            "module": "utils_py",
            "status": "interpreted",
            "value": 10
        },
        "aggregator_py": {
            "module": "aggregator_py",
            "sum": 52,
            "dependencies_met": True
        },
        "final_cpp": {
            "module": "final_cpp",
            "complete": True
        }
    }

    # Check that all expected keys exist
    for key, expected_val in expected_data.items():
        assert key in report_data, f"Project '{key}' is missing from the final report."
        assert report_data[key] == expected_val, f"Data for project '{key}' is incorrect. Expected {expected_val}, got {report_data[key]}."

    # Check that no extra keys exist
    for key in report_data.keys():
        assert key in expected_data, f"Unexpected project '{key}' found in the final report."

def test_individual_outputs_exist():
    # If the build script ran correctly, these outputs should be present in the monorepo subdirectories.
    projects = ["core_cpp", "utils_py", "aggregator_py", "final_cpp"]

    for project in projects:
        output_path = os.path.join(MONOREPO_PATH, project, "output.json")
        assert os.path.isfile(output_path), f"The build output file {output_path} is missing. Did the build step for {project} run?"