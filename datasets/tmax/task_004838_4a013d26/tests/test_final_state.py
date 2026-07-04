# test_final_state.py

import os
import subprocess
import pytest

def test_process_binding_script_fixed():
    script_path = "/home/user/process_binding.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    # Check that some form of sorting is introduced
    # The simplest check is the presence of 'sort' or a wildcard expansion that implies sorting
    assert "sort" in content or "ls " in content or "*.csv" in content.replace('"', ''), \
        f"Script {script_path} does not seem to contain sorting logic (e.g., 'sort')."

def test_process_binding_output():
    script_path = "/home/user/process_binding.sh"
    try:
        result = subprocess.run([script_path], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        assert output == "1.18571", f"Expected script to output '1.18571', but got '{output}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script {script_path} failed to execute: {e.stderr}")

def test_test_hypothesis_script_exists_and_executable():
    script_path = "/home/user/test_hypothesis.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_result_txt_content():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read()

    assert content == "H0: Weak Binding\n", f"Expected result.txt to contain exactly 'H0: Weak Binding\\n', but got {repr(content)}"