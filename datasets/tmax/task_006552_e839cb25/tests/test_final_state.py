# test_final_state.py

import os
import stat
import pytest

def test_resource_compiler_exists_and_executable():
    path = "/home/user/resource_compiler.sh"
    assert os.path.exists(path), f"The script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {path} is not executable."

def test_res_map_generated_correctly():
    path = "/home/user/build/res_map.sh"
    assert os.path.exists(path), f"The file {path} was not generated."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        'export APP_NAME="MyApp"',
        'export ENABLE_LOGS="true"',
        'export API_ENDPOINT="https://api.example.com"',
        'export USER_ONBOARDING="false"'
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {path}."

def test_test_res_exists_and_executable():
    path = "/home/user/tests/test_res.sh"
    assert os.path.exists(path), f"The test stub {path} was not generated."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The test stub {path} is not executable."

    with open(path, "r") as f:
        content = f.read()

    assert "#!/bin/bash" in content, f"Shebang missing in {path}."
    assert "source /home/user/build/res_map.sh" in content, f"Source command missing in {path}."

def test_test_results_log_generated_correctly():
    path = "/home/user/build/test_results.log"
    assert os.path.exists(path), f"The log file {path} was not generated."

    with open(path, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "PASS: APP_NAME",
        "PASS: ENABLE_LOGS",
        "PASS: API_ENDPOINT",
        "PASS: USER_ONBOARDING"
    ]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, got {len(content)}."
    for i, expected in enumerate(expected_lines):
        assert content[i].strip() == expected, f"Expected line {i+1} to be '{expected}', got '{content[i].strip()}'."