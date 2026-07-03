# test_final_state.py
import os
import subprocess
import pytest

def test_script_recovered():
    script_file = "/home/user/scripts/calc_billing.py"
    assert os.path.isfile(script_file), f"The script {script_file} was not recovered."

def test_billing_result_correct():
    result_file = "/home/user/billing_result.txt"
    assert os.path.isfile(result_file), f"The result file {result_file} is missing."

    with open(result_file, 'r') as f:
        content = f.read().strip()

    assert content == "800.0", f"Expected billing result to be '800.0', but got '{content}'."

def test_script_execution():
    script_file = "/home/user/scripts/calc_billing.py"
    data_file = "/home/user/data/january_usage.json"

    assert os.path.isfile(script_file), "Script file is missing, cannot test execution."
    assert os.path.isfile(data_file), "Data file is missing, cannot test execution."

    # Check if the script runs and produces the correct output
    try:
        output = subprocess.check_output(["python3", script_file, data_file], text=True)
        result = output.strip()
        assert result == "800.0", f"Executing the recovered script produced '{result}' instead of '800.0'. The bugs might not be fully fixed."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing the recovered script failed with error: {e}")