# test_final_state.py
import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/build_and_test.sh"

@pytest.fixture(scope="session", autouse=True)
def run_script():
    """Ensure the script exists, is executable, and run it to produce artifacts."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"Script {SCRIPT_PATH} is not executable."

    # Execute the script as the user would
    result = subprocess.run(["bash", SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script executed with non-zero exit code.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

def test_shared_library_created():
    lib_path = "/home/user/lib/libdataproc.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not created."

    # Verify it is a shared object
    result = subprocess.run(["file", lib_path], capture_output=True, text=True)
    assert "shared object" in result.stdout.lower(), f"{lib_path} is not compiled as a shared object."

def test_test_runner_created():
    bin_path = "/home/user/bin/test_runner"
    assert os.path.isfile(bin_path), f"Executable {bin_path} was not created."

    st = os.stat(bin_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"{bin_path} is not executable."

def test_test_results_json():
    res_path = "/home/user/test_results.json"
    assert os.path.isfile(res_path), f"Results file {res_path} was not created."

    with open(res_path, "r") as f:
        content = f.read()

    assert content.strip() == '{"value": 42}', f"Unexpected content in {res_path}: {content!r}"

def test_status_log():
    log_path = "/home/user/status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read()

    assert content.strip() == "PASS", f"Unexpected content in {log_path}: {content!r}"