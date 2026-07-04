# test_final_state.py
import os
import json
import pytest

def test_e2e_result():
    result_path = "/home/user/workspace/e2e_result.json"
    assert os.path.isfile(result_path), f"File {result_path} is missing. Did the e2e test script run and create it?"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} does not contain valid JSON.")

    assert "failed_files" in data, "The JSON response is missing the 'failed_files' key."
    assert isinstance(data["failed_files"], list), "'failed_files' should be a list."

    expected_failed = ["app.log", "missing.txt"]
    assert data["failed_files"] == expected_failed, f"Expected failed_files to be {expected_failed}, but got {data['failed_files']}"

def test_app_py_import_fixed():
    app_py_path = "/home/user/workspace/api/app.py"
    assert os.path.isfile(app_py_path), f"File {app_py_path} is missing."
    with open(app_py_path, "r") as f:
        content = f.read()

    # The broken import was `from hashing import verify_checksums`
    # Just check that it's no longer the exact broken import
    assert "from hashing import verify_checksums" not in content, "The import in app.py is still broken (still using 'from hashing import verify_checksums')."

    try:
        compile(content, app_py_path, 'exec')
    except SyntaxError as e:
        pytest.fail(f"Syntax error in app.py: {e}")

def test_test_e2e_py_exists():
    test_e2e_path = "/home/user/workspace/test_e2e.py"
    assert os.path.isfile(test_e2e_path), f"File {test_e2e_path} is missing. The orchestrating script was not created."

    with open(test_e2e_path, "r") as f:
        content = f.read()

    try:
        compile(content, test_e2e_path, 'exec')
    except SyntaxError as e:
        pytest.fail(f"Syntax error in test_e2e.py: {e}")