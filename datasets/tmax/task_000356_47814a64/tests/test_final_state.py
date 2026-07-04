# test_final_state.py

import os
import subprocess
import pytest

def test_fixed_variance_log():
    log_path = "/home/user/fixed_variance.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "0.000000", f"Expected variance to be '0.000000', but got '{content}'."

def test_regression_test_script():
    script_path = "/home/user/regression_test.sh"
    assert os.path.isfile(script_path), f"Regression test script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Regression test script {script_path} is not executable."

    # Run the regression test
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Regression test script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_uptime_monitor_c_fixed():
    c_file = "/home/user/uptime_monitor.c"
    assert os.path.isfile(c_file), f"Source file {c_file} is missing."

    # Compile the C code
    exe_path = "/tmp/uptime_monitor_test"
    compile_result = subprocess.run(
        ["gcc", "-O2", c_file, "-lm", "-o", exe_path],
        capture_output=True, text=True
    )
    assert compile_result.returncode == 0, f"Failed to compile {c_file}:\n{compile_result.stderr}"

    # Create the bad state file
    state_file = "/home/user/state.txt"
    with open(state_file, "w") as f:
        f.write("1000 1000000000.0 1000000000000000.0\n")

    # Run the compiled executable with the new latency
    run_result = subprocess.run(
        [exe_path, "1000000.0"],
        capture_output=True, text=True
    )
    assert run_result.returncode == 0, f"Executable failed with exit code {run_result.returncode}.\nStderr: {run_result.stderr}"

    output = run_result.stdout.strip()
    assert output != "NaN", "The C program still outputs 'NaN' for the bad state."
    assert output == "0.000000", f"Expected output to be '0.000000', but got '{output}'."