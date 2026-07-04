# test_final_state.py

import os
import re
import subprocess
import pytest

def test_build_sh_configured():
    path = "/home/user/sim_daemon/build.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()

    assert re.search(r'SIM_ENV=production', content), "build.sh does not set SIM_ENV=production."
    assert "export SIM_ENV" in content or "export SIM_ENV=production" in content or re.search(r'^SIM_ENV=production\s+g\+\+', content, re.MULTILINE), "build.sh does not export SIM_ENV."

def test_sim_server_cpp_fixes():
    path = "/home/user/sim_daemon/sim_server.cpp"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()

    # Check for cassert
    assert "<cassert>" in content, "sim_server.cpp does not include <cassert>."

    # Check for assert
    assert "assert(states.size() <= 1000);" in content.replace(" ", ""), "sim_server.cpp does not contain the required assertion."

    # Check for loop condition fix
    assert "time != target_time" not in content, "The buggy floating-point equality check is still present."
    assert "time < target_time" in content or "time <= target_time" in content or "time<target_time" in content.replace(" ", ""), "Loop condition was not properly fixed to use < or <=."

    # Check for memory leak fix
    assert "delete" in content, "No 'delete' found in sim_server.cpp, memory leak is likely not fixed."

def test_regression_script_exists_and_succeeds():
    script_path = "/home/user/test.sh"
    assert os.path.isfile(script_path), f"Regression test script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Regression test script {script_path} is not executable."

    # Ensure the input file exists for the test script just in case the script relies on it being there
    input_file = "/home/user/test_input.txt"
    if not os.path.exists(input_file):
        with open(input_file, 'w') as f:
            f.write("1.0\n")

    # Run the test script
    result = subprocess.run(["/bin/bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"test.sh failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Verify valgrind output file exists and has no leaks
    valgrind_out = "/home/user/valgrind_out.txt"
    assert os.path.isfile(valgrind_out), f"Valgrind output file {valgrind_out} was not created."
    with open(valgrind_out, 'r') as f:
        v_content = f.read()

    assert "0 bytes in 0 blocks" in v_content, "Valgrind output does not report '0 bytes in 0 blocks' definitely lost."