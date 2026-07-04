# test_final_state.py

import os
import json
import stat
import pytest

def test_evaluator_c_exists():
    path = "/home/user/evaluator.c"
    assert os.path.isfile(path), f"File {path} is missing."

def test_build_and_test_sh_exists_and_executable():
    path = "/home/user/build_and_test.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_evaluator_executable_exists():
    path = "/home/user/evaluator"
    assert os.path.isfile(path), f"Compiled executable {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_test_result_json_exists_and_correct():
    path = "/home/user/test_result.json"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {path} is not valid JSON: {content}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("result") == 500, f"Expected result 500, got {data.get('result')}"