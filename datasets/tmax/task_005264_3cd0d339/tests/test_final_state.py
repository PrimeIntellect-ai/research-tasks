# test_final_state.py

import os
import subprocess
import pytest

def test_find_cycles_script_execution():
    script_path = '/home/user/find_cycles.py'
    assert os.path.exists(script_path), f"Python script {script_path} does not exist."

    # Execute the script to ensure it generates the log file
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {script_path} failed with error:\n{result.stderr}"

def test_cycles_log_content():
    log_path = '/home/user/cycles.log'
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. The script might not have created it."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ['1,2,3,4', '10,20,30,40']

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} cycles, but found {len(lines)}."
    assert lines == expected_lines, f"Content of {log_path} does not match expected output.\nExpected: {expected_lines}\nGot: {lines}"

def test_optimize_sql_content():
    sql_path = '/home/user/optimize.sql'
    assert os.path.exists(sql_path), f"SQL script {sql_path} does not exist."

    with open(sql_path, 'r') as f:
        content = f.read().lower()

    assert 'create index' in content, f"No 'CREATE INDEX' statement found in {sql_path}."
    assert 'sender_id' in content, f"'sender_id' column not found in the index definition in {sql_path}."
    assert 'receiver_id' in content, f"'receiver_id' column not found in the index definition in {sql_path}."