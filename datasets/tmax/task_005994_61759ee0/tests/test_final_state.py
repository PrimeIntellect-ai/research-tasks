# test_final_state.py

import os
import stat
import subprocess
import sys
import importlib.util

PROJECT_DIR = "/home/user/project"
PATCH_FILE = os.path.join(PROJECT_DIR, "pipeline.patch")
CI_SCRIPT = os.path.join(PROJECT_DIR, "run_ci.sh")
TEST_FILE = os.path.join(PROJECT_DIR, "test_processor.py")
PY_FILE = os.path.join(PROJECT_DIR, "pipeline_util.py")

def test_patch_file_exists_and_valid():
    assert os.path.isfile(PATCH_FILE), f"Patch file {PATCH_FILE} does not exist."
    with open(PATCH_FILE, 'r') as f:
        content = f.read()
    assert "---" in content and "+++" in content, "Patch file does not appear to be a unified diff."
    assert "pipeline_util.py" in content, "Patch file does not reference pipeline_util.py."

def test_test_processor_exists_and_uses_hypothesis():
    assert os.path.isfile(TEST_FILE), f"Test file {TEST_FILE} does not exist."
    with open(TEST_FILE, 'r') as f:
        content = f.read()
    assert "hypothesis" in content, "Test file does not seem to import/use hypothesis."
    assert "pytest" in content, "Test file does not seem to import/use pytest."

def test_run_ci_script():
    assert os.path.isfile(CI_SCRIPT), f"CI script {CI_SCRIPT} does not exist."
    st = os.stat(CI_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"CI script {CI_SCRIPT} is not executable."

    # Run the CI script
    result = subprocess.run([CI_SCRIPT], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"run_ci.sh failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert "CI PASS" in result.stdout, "run_ci.sh did not print 'CI PASS' to standard output."

def test_process_string_py_logic():
    assert os.path.isfile(PY_FILE), f"Python file {PY_FILE} does not exist."

    # Dynamically load the module
    spec = importlib.util.spec_from_file_location("pipeline_util", PY_FILE)
    pipeline_util = importlib.util.module_from_spec(spec)
    sys.modules["pipeline_util"] = pipeline_util
    try:
        spec.loader.exec_module(pipeline_util)
    except Exception as e:
        assert False, f"Failed to import {PY_FILE}: {e}"

    assert hasattr(pipeline_util, "process_string_py"), f"process_string_py function not found in {PY_FILE}."

    # Test the logic
    process_string_py = pipeline_util.process_string_py

    test_cases = [
        ("hello", "OllEh"),
        ("abcde", "EdcbA"),
        ("aeiou", "UOIEA"),
        ("XYZ", "ZYX"),
        ("123", "321"),
        ("", "")
    ]

    for inp, expected in test_cases:
        out = process_string_py(inp)
        assert out == expected, f"process_string_py({inp!r}) returned {out!r}, expected {expected!r}."