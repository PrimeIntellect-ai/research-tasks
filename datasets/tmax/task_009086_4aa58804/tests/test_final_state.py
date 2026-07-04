# test_final_state.py
import os
import stat
import subprocess
import time
import pytest

SCRIPT_PATH = "/home/user/build.sh"

def test_build_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"File {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file."
    st = os.stat(SCRIPT_PATH)
    assert st.st_mode & stat.S_IXUSR, f"File {SCRIPT_PATH} is not executable by the user."

def test_build_script_backgrounding_retained():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    # The script must still use backgrounding for the process_asset function
    assert "&" in content, "Backgrounding (&) was removed from the script. Compilation must remain parallel."

def test_build_script_execution_success_and_no_hang():
    # Run the script multiple times to ensure race conditions and hangs are fixed
    for attempt in range(3):
        try:
            result = subprocess.run(
                [SCRIPT_PATH, "50"],
                capture_output=True,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Attempt {attempt + 1}: Script timed out after 5 seconds. The infinite loop or a deadlock is still present.")

        assert result.returncode == 0, (
            f"Attempt {attempt + 1}: Script failed with return code {result.returncode}.\n"
            f"Stdout: {result.stdout}\n"
            f"Stderr: {result.stderr}"
        )
        assert "Success: 50" in result.stdout, (
            f"Attempt {attempt + 1}: Expected 'Success: 50' in stdout, got: {result.stdout}"
        )