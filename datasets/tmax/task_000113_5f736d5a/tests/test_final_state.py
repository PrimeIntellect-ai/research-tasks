# test_final_state.py

import os
import json
import pytest

WORKSPACE_DIR = '/home/user/workspace'
ARTIFACTS_DIR = os.path.join(WORKSPACE_DIR, 'artifacts')
CPP_ARTIFACT = os.path.join(ARTIFACTS_DIR, 'cpp_artifact')
RUST_ARTIFACT = os.path.join(ARTIFACTS_DIR, 'rust_artifact')
TEST_RESULTS_JSON = os.path.join(WORKSPACE_DIR, 'test_results.json')
TEST_PIPELINE_PY = os.path.join(WORKSPACE_DIR, 'test_pipeline.py')

def test_test_pipeline_script_exists():
    assert os.path.isfile(TEST_PIPELINE_PY), f"Expected python script {TEST_PIPELINE_PY} is missing."

def test_artifacts_directory_exists():
    assert os.path.isdir(ARTIFACTS_DIR), f"Expected artifacts directory {ARTIFACTS_DIR} is missing."

def test_cpp_artifact_exists_and_executable():
    assert os.path.isfile(CPP_ARTIFACT), f"C++ artifact {CPP_ARTIFACT} is missing."
    assert os.access(CPP_ARTIFACT, os.X_OK), f"C++ artifact {CPP_ARTIFACT} is not executable."

def test_rust_artifact_exists_and_executable():
    assert os.path.isfile(RUST_ARTIFACT), f"Rust artifact {RUST_ARTIFACT} is missing."
    assert os.access(RUST_ARTIFACT, os.X_OK), f"Rust artifact {RUST_ARTIFACT} is not executable."

def test_test_results_json():
    assert os.path.isfile(TEST_RESULTS_JSON), f"Test results JSON {TEST_RESULTS_JSON} is missing."

    with open(TEST_RESULTS_JSON, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{TEST_RESULTS_JSON} is not valid JSON.")

    expected_keys = {
        "build_cpp_success",
        "build_rust_success",
        "test_validation_missing_header_success",
        "test_rate_limit_success"
    }

    for key in expected_keys:
        assert key in data, f"Key '{key}' is missing from {TEST_RESULTS_JSON}."
        assert data[key] is True, f"Key '{key}' in {TEST_RESULTS_JSON} is not True."