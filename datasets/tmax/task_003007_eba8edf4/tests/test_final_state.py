# test_final_state.py

import os
import subprocess
import pytest

def test_etl_c_exists():
    assert os.path.isfile("/home/user/etl_task/etl.c"), "etl.c is missing. You must write the C program."

def test_etl_binary_exists_and_executable():
    binary_path = "/home/user/etl_task/etl"
    assert os.path.isfile(binary_path), "Compiled etl binary is missing. Did you compile etl.c?"
    assert os.access(binary_path, os.X_OK), "etl binary is not executable."

def test_reduced_data_csv():
    csv_path = "/home/user/etl_task/reduced_data.csv"
    assert os.path.isfile(csv_path), "reduced_data.csv is missing. Did you run the etl program?"

    with open(csv_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "UserID,P1,P2\n"
        "1,-0.30,2.30\n"
        "2,2.40,0.30\n"
        "3,1.20,1.40"
    )

    assert content == expected_content, f"Content of {csv_path} does not match the expected output. Got:\n{content}"

def test_validate_sh():
    script_path = "/home/user/etl_task/validate.sh"
    assert os.path.isfile(script_path), "validate.sh is missing."
    assert os.access(script_path, os.X_OK), "validate.sh is not executable."

    # Run the script and check output and return code
    # We assume reduced_data.csv is already correctly generated based on previous test
    result = subprocess.run([script_path], cwd="/home/user/etl_task", capture_output=True, text=True)

    assert result.returncode == 0, f"validate.sh did not exit with code 0. Exit code: {result.returncode}"
    assert result.stdout.strip() == "VALID", f"validate.sh did not print 'VALID'. Output: {result.stdout.strip()}"