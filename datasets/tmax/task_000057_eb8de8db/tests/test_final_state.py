# test_final_state.py

import os
import stat
import time
import subprocess
import pytest

def test_run_tests_script_exists_and_executable():
    script_path = "/home/user/run_tests.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"Script {script_path} is not executable."

def test_bats_exec_suite_fixed():
    file_path = "/app/bats-core-1.8.2/libexec/bats-core/bats-exec-suite"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    with open(file_path, "r") as f:
        content = f.read()
    # We check that the specific perturbation line is removed
    assert "jobs=1 # DEBUG: force single job" not in content, f"The perturbation 'jobs=1' is still present in {file_path}."

def test_execution_time_and_correctness():
    script_path = "/home/user/run_tests.sh"
    assert os.path.isfile(script_path), "Cannot measure execution time because script does not exist."

    start_time = time.time()
    # Run the script as the user
    result = subprocess.run(["sudo", "-u", "user", "bash", script_path], capture_output=True, text=True)
    end_time = time.time()

    execution_time = end_time - start_time

    assert result.returncode == 0, f"Tests failed or script errored. Return code: {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Verify that the test suite actually ran the 24 tests
    output = result.stdout + "\n" + result.stderr
    assert "24 tests" in output or "ok 24" in output, "The script output does not indicate that 24 tests were run. Did it execute the bats test suite?"

    assert execution_time <= 6.0, f"Execution time {execution_time:.2f}s exceeded threshold of 6.0s. The test suite is likely not running in parallel."