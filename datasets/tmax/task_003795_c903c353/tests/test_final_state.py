# test_final_state.py
import os
import subprocess
import pytest

def test_final_output_log():
    log_path = "/home/user/query_engine/final_output.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_line = 'ID=3 USER="admin" OR STATUS=500 MESSAGE="Critical failure in auth module"'
    assert expected_line in content, f"Expected output not found in {log_path}. Found: {content}"

def test_fuzz_sh_executable():
    fuzz_path = "/home/user/query_engine/fuzz.sh"
    assert os.path.isfile(fuzz_path), f"{fuzz_path} does not exist."
    assert os.access(fuzz_path, os.X_OK), f"{fuzz_path} is not executable."

def test_regression_test_sh_executable_and_passes():
    reg_test_path = "/home/user/query_engine/regression_test.sh"
    assert os.path.isfile(reg_test_path), f"{reg_test_path} does not exist."
    assert os.access(reg_test_path, os.X_OK), f"{reg_test_path} is not executable."

    result = subprocess.run([reg_test_path], cwd="/home/user/query_engine", capture_output=True)
    assert result.returncode == 0, f"{reg_test_path} failed with exit code {result.returncode}. Stderr: {result.stderr.decode()}"

def test_query_sh_safe_evaluation():
    query_path = "/home/user/query_engine/query.sh"
    assert os.path.isfile(query_path), f"{query_path} does not exist."
    assert os.access(query_path, os.X_OK), f"{query_path} is not executable."

    # Test with a special character query that would break eval
    test_query = "test*"
    result = subprocess.run([query_path, test_query], cwd="/home/user/query_engine", capture_output=True, text=True)

    assert result.returncode == 0, f"{query_path} failed on safe evaluation test. Stderr: {result.stderr}"
    assert "Wildcard test" in result.stdout, "query.sh did not return the expected result for special character query."

    # Test with a query that has spaces and quotes
    test_query2 = 'USER="admin"'
    result2 = subprocess.run([query_path, test_query2], cwd="/home/user/query_engine", capture_output=True, text=True)
    assert result2.returncode == 0, f"{query_path} failed on quotes test."
    assert "Login successful" in result2.stdout, "query.sh did not return expected result for quotes query."