# test_final_state.py

import os
import subprocess
import pytest

def test_etl_script_exists_and_executable():
    script_path = "/home/user/etl.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_test_etl_script_exists_and_executable():
    script_path = "/home/user/test_etl.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_etl_script_execution_and_output():
    input_file = "/home/user/raw_events.csv"
    output_file = "/home/user/summary.csv"
    script_path = "/home/user/etl.sh"

    # Remove output file if it exists to ensure we test the script's creation of it
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the ETL script
    result = subprocess.run(["bash", script_path, input_file, output_file], capture_output=True, text=True)
    assert result.returncode == 0, f"The script {script_path} failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.exists(output_file), f"The script did not create the output file at {output_file}."

    expected_output = """Token,Sum,ValidCount,Mean
alpha,35,3,11.67
beta,25,2,12.50
delta,20,2,10.00
gamma,15,1,15.00"""

    with open(output_file, 'r') as f:
        content = f.read().strip()

    assert content == expected_output, f"The content of {output_file} does not match the expected output.\nExpected:\n{expected_output}\n\nGot:\n{content}"

def test_test_etl_script_execution():
    script_path = "/home/user/test_etl.sh"

    # Run the test script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"The test script {script_path} failed with return code {result.returncode}."
    assert "PASS" in result.stdout, f"The test script did not print 'PASS'. Output: {result.stdout}"