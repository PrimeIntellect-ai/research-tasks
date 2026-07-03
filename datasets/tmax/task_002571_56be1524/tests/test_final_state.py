# test_final_state.py

import os
import stat
import subprocess
import pytest

PIPELINE_DIR = "/home/user/pipeline"
C_FILE = os.path.join(PIPELINE_DIR, "calc_interp.c")
PY_FILE = os.path.join(PIPELINE_DIR, "run_data.py")
CSV_FILE = os.path.join(PIPELINE_DIR, "data.csv")
CI_SCRIPT = os.path.join(PIPELINE_DIR, "ci_build.sh")
CI_LOG = os.path.join(PIPELINE_DIR, "ci_output.log")
EXECUTABLE = os.path.join(PIPELINE_DIR, "calc_interp")

def test_c_file_fixed():
    assert os.path.isfile(C_FILE), f"File {C_FILE} is missing."
    with open(C_FILE, "r") as f:
        content = f.read()

    # Check that addition actually adds
    # The original bug was `printf("%d\n", a - b); // BUG: Should be a + b`
    # We should look for `a + b` in the block checking for '+'
    assert "a + b" in content, f"The C file {C_FILE} does not seem to have 'a + b' to fix the addition bug."

def test_ci_build_script_exists_and_executable():
    assert os.path.isfile(CI_SCRIPT), f"CI script {CI_SCRIPT} is missing."
    st = os.stat(CI_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"CI script {CI_SCRIPT} is not executable."

def test_ci_output_log_correct():
    assert os.path.isfile(CI_LOG), f"Output log {CI_LOG} is missing. Did you run the CI script?"
    with open(CI_LOG, "r") as f:
        content = f.read().strip()

    expected_output = "Result: 25\nResult: 20\nResult: 58"

    # Allow for b'25' if they didn't decode, but the prompt says:
    # "Let's accept a decoded version for strict verification"
    # Actually, the prompt says "Strict Expected File... Result: 25"

    assert content == expected_output, f"The contents of {CI_LOG} do not match the expected output.\nExpected:\n{expected_output}\nGot:\n{content}"

def test_python_script_is_python3():
    assert os.path.isfile(PY_FILE), f"File {PY_FILE} is missing."
    # We can check if it compiles under python3
    try:
        subprocess.check_call(["python3", "-m", "py_compile", PY_FILE])
    except subprocess.CalledProcessError:
        pytest.fail(f"The script {PY_FILE} is not valid Python 3 code.")

def test_executable_compiled():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} is missing. The CI script should compile it."
    st = os.stat(EXECUTABLE)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {EXECUTABLE} is not executable."