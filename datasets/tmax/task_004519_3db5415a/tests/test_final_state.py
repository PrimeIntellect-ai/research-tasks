# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    """Test that the script /home/user/process_data.sh exists and is executable."""
    script_path = '/home/user/process_data.sh'
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_output_directory_exists():
    """Test that the output directory was created."""
    assert os.path.isdir('/home/user/output'), "/home/user/output directory is missing."

def test_output_file_exists():
    """Test that the output CSV file exists."""
    output_file = '/home/user/output/clean_rolling_tx.csv'
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

def test_output_file_content():
    """Test that the output CSV file has the exact expected content."""
    output_file = '/home/user/output/clean_rolling_tx.csv'

    expected_content = """tx_id,user_id,amount,rolling_sum
T01,U1,100,100
T04,U1,50,150
T03,U2,200,200
T05,U2,300,500
T07,U3,50,50
T08,U3,50,100
T09,U3,50,100"""

    with open(output_file, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {output_file} does not match the expected output."