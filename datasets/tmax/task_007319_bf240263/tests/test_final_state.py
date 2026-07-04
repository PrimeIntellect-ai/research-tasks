# test_final_state.py

import os
import subprocess
import pytest

def test_results_log():
    """
    Validates that results.log exists and contains the correct outputs
    from the batch script, indicating that both the script and the 
    library dependency have been fixed.
    """
    log_file = "/home/user/project/results.log"
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    with open(log_file, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "input1.txt: 10.280000",
        "input 2.txt: 22.280000"
    ]

    for line in expected_lines:
        assert line in content, f"Expected output '{line}' not found in results.log. Is the script fixed and poly_eval correctly linked?"

def test_verify_c_exists_and_content():
    """
    Validates that verify.c exists and contains the required function calls.
    """
    verify_c = "/home/user/project/verify.c"
    assert os.path.isfile(verify_c), f"C file missing: {verify_c}"

    with open(verify_c, "r") as f:
        content = f.read()

    assert "dlopen" in content, "verify.c must use dlopen() to dynamically load the library"
    assert "dlsym" in content, "verify.c must use dlsym() to resolve the function"
    assert "assert" in content, "verify.c must use assert() to validate the result"

def test_verify_c_compiles_and_runs():
    """
    Validates that verify.c compiles successfully and passes its assertion.
    """
    verify_c = "/home/user/project/verify.c"
    assert os.path.isfile(verify_c), f"C file missing: {verify_c}"

    out_bin = "/tmp/verify_test"

    # Compile the C program
    compile_cmd = ["gcc", "-o", out_bin, verify_c, "-ldl"]
    compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_result.returncode == 0, f"verify.c failed to compile:\n{compile_result.stderr}"

    # Run the compiled binary
    run_result = subprocess.run([out_bin], capture_output=True, text=True)
    assert run_result.returncode == 0, f"verify.c failed to run (crashed or assertion failed):\n{run_result.stderr}\n{run_result.stdout}"