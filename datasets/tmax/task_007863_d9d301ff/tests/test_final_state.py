# test_final_state.py

import os
import stat
import subprocess
import re

def test_test_calc_script_exists_and_executable():
    script_path = "/home/user/test_calc.sh"
    assert os.path.isfile(script_path), f"The file {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file {script_path} is not executable."

def test_calc_service_fixed_memory_leak():
    script_path = "/home/user/calc_service.sh"
    assert os.path.isfile(script_path), f"The file {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # Check that LOG_BUFFER accumulation is removed
    assert "LOG_BUFFER+=" not in content, "The memory leak bug (LOG_BUFFER+=) is still present in the service script."

    # Check that it appends to the log file
    assert re.search(r">>\s*/home/user/service\.log", content), "The service script does not appear to append (>>) to /home/user/service.log."

def test_test_calc_script_execution():
    script_path = "/home/user/test_calc.sh"

    # Run the test script
    try:
        result = subprocess.run(
            [script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        assert False, f"Execution of {script_path} timed out."

    assert result.returncode == 0, f"{script_path} exited with code {result.returncode}, expected 0. Stderr: {result.stderr}"
    assert "PASS" in result.stdout, f"{script_path} did not print 'PASS'. Stdout: {result.stdout}"