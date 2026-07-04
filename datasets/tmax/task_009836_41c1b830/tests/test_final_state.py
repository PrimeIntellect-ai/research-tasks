# test_final_state.py
import os
import json
import pytest

def test_test_results_json():
    json_path = '/home/user/project/test_results.json'
    assert os.path.isfile(json_path), f"The file {json_path} does not exist. Did you run your test script?"

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert "tests_run" in results, "Key 'tests_run' missing in test_results.json"
    assert "failures" in results, "Key 'failures' missing in test_results.json"
    assert "errors" in results, "Key 'errors' missing in test_results.json"

    assert results["tests_run"] >= 2, f"Expected at least 2 tests run, got {results['tests_run']}"
    assert results["failures"] == 0, f"Expected 0 failures, got {results['failures']}"
    assert results["errors"] == 0, f"Expected 0 errors, got {results['errors']}"

def test_test_builder_py_content():
    py_path = '/home/user/project/test_builder.py'
    assert os.path.isfile(py_path), f"The file {py_path} does not exist."

    with open(py_path, 'r') as f:
        content = f.read()

    assert "mock" in content, "test_builder.py does not seem to use 'mock' as required."
    assert "imul" in content, "test_builder.py does not seem to check for the 'imul' instruction."
    assert "unittest" in content, "test_builder.py does not seem to use 'unittest'."