# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_dropper_build_fixed():
    script_path = "/home/user/dropper_build.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Run the script 50 times to ensure intermittent failure is resolved
    for i in range(50):
        result = subprocess.run([script_path], capture_output=True)
        assert result.returncode == 0, f"Script failed on run {i+1} with exit code {result.returncode}. Stderr: {result.stderr.decode()}"

def test_dropper_build_content_fix():
    script_path = "/home/user/dropper_build.sh"
    with open(script_path, 'r') as f:
        content = f.read()

    # The original buggy line was: PAYLOAD_SIZE=$(( 10000 / (RANDOM % 5) ))
    # We should ensure the division by zero is fixed by adding 1.
    assert "PAYLOAD_SIZE=" in content, "PAYLOAD_SIZE assignment missing."
    assert "+ 1" in content or "+1" in content, "The fix must add 1 to the random modulus result."

def test_mre_script_exists_and_executable():
    mre_path = "/home/user/mre.sh"
    assert os.path.isfile(mre_path), f"MRE script {mre_path} does not exist."

    st = os.stat(mre_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"MRE script {mre_path} is not executable."

def test_mre_script_behavior():
    mre_path = "/home/user/mre.sh"

    # Run the MRE script
    result = subprocess.run([mre_path], capture_output=True, text=True)

    # It must exit with status code 1
    assert result.returncode == 1, f"MRE script exited with code {result.returncode}, expected 1."

    # Standard error must contain division by zero error
    assert "division by 0" in result.stderr.lower(), "Stderr did not contain 'division by 0' error."

    # Standard output must be suppressed (could have minor output depending on loop implementation, but the arithmetic output shouldn't be there)
    # The requirement is "Suppress standard output but allow standard error to be printed."
    assert result.stdout.strip() == "", "Standard output was not suppressed."