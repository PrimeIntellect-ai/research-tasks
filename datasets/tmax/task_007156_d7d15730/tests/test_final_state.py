# test_final_state.py

import os
import subprocess
import stat
import pytest

def test_regression_script_exists_and_executable():
    script_path = "/home/user/test_regression.sh"
    assert os.path.isfile(script_path), f"Regression script {script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Regression script {script_path} is not executable."

def test_regression_script_contents():
    script_path = "/home/user/test_regression.sh"
    assert os.path.isfile(script_path), f"Regression script {script_path} is missing."
    with open(script_path, "r") as f:
        content = f.read()

    # Check for CONF_PATH
    assert "CONF_PATH=/home/user/conf" in content, "The script does not set the CONF_PATH correctly."
    assert "timeout" in content, "The script does not use the 'timeout' command."
    assert "g++" in content, "The script does not compile the parser with 'g++'."

def test_parser_cpp_fixed():
    parser_path = "/home/user/parser.cpp"
    assert os.path.isfile(parser_path), f"Source file {parser_path} is missing."
    with open(parser_path, "r") as f:
        content = f.read()

    # Check that there is some form of check for chunk_size == 0 or break condition
    # The user might write `if (chunk_size == 0) break;` or similar
    # We will just verify the regression script passes, but we can also do a loose check.
    assert "chunk_size" in content, "The chunk_size variable is missing."

def test_regression_script_execution():
    script_path = "/home/user/test_regression.sh"
    assert os.path.isfile(script_path), f"Regression script {script_path} is missing."

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)

    assert result.returncode == 0, f"Regression script failed with exit code {result.returncode}. Stderr: {result.stderr}"

    stdout = result.stdout.strip()
    assert stdout.endswith("PASS"), f"Regression script did not print PASS. Output: {stdout}"