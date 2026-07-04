# test_final_state.py

import os
import subprocess
import pytest

def test_etl_script_exists_and_executable():
    script_path = "/home/user/etl.sh"
    assert os.path.isfile(script_path), f"Missing file: {script_path}"
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_etl_script_reads_weights():
    script_path = "/home/user/etl.sh"
    with open(script_path, "r") as f:
        content = f.read()
    assert "weights.txt" in content, "The script does not appear to read from weights.txt dynamically."

def test_etl_execution_and_output():
    script_path = "/home/user/etl.sh"
    output_path = "/home/user/output.csv"

    # Remove output if it exists to ensure we are testing the script's execution
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    assert os.path.isfile(output_path), f"Script did not create {output_path}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = """id,score
1,115
2,50
3,-18
4,0
5,16
6,0
7,-32
8,6
9,51
10,-19"""

    assert content == expected_content, f"Output CSV does not match expected values. Got:\n{content}"