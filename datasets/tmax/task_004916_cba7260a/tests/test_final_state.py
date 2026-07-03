# test_final_state.py
import os
import subprocess
import pytest

def test_test_results_log():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run the tests and redirect output?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "ALL TESTS PASSED", f"Expected log file to contain 'ALL TESTS PASSED', but got: {content}"

def test_validator_cpp_fixes():
    cpp_path = "/home/user/validator.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read()

    # Check that the rate limit threshold was updated to 100
    assert ">= 100" in content, "The rate limit threshold in check_rate_limit was not correctly updated to 100."

    # Check that the regex was updated to include quotes around the data value
    assert '\"[a-zA-Z]+\"' in content or r'\"[a-zA-Z]+\"' in content or '"[a-zA-Z]+"' in content or r'\"[a-zA-Z]+\"' in content.replace('\\"', '"'), "The regex in validate_payload does not correctly account for the string quotes around the data value."

def test_compilation_and_execution():
    # Compile the files to ensure they are valid and tests pass
    compile_cmd = [
        "g++", "-std=c++17", 
        "/home/user/test_validator.cpp", 
        "/home/user/validator.cpp", 
        "-o", "/tmp/verify_test"
    ]

    compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_result.returncode == 0, f"Compilation failed:\n{compile_result.stderr}"

    run_result = subprocess.run(["/tmp/verify_test"], capture_output=True, text=True)
    assert run_result.returncode == 0, f"Running the compiled executable failed (assertion error likely):\n{run_result.stderr}"
    assert "ALL TESTS PASSED" in run_result.stdout, "The executable did not output the expected success message."