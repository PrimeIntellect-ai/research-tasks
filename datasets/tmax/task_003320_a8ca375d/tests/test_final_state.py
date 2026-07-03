# test_final_state.py

import os
import subprocess
import pytest

def test_processed_data_csv_correct():
    file_path = "/home/user/processed_data.csv"
    assert os.path.isfile(file_path), f"File missing: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = """id,out1,out2,out3
1,1.5000,2.4000,3.8000
2,3.9000,6.9000,8.3000
3,6.3000,11.4000,12.8000"""

    assert content == expected_content, f"Content of {file_path} does not match expected output."

def test_etl_c_exists():
    file_path = "/home/user/etl.c"
    assert os.path.isfile(file_path), f"C source file missing: {file_path}"

def test_pipeline_script():
    script_path = "/home/user/test_pipeline.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    # Run the script and check output
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed with return code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert "PIPELINE PASS" in output, f"Script did not print 'PIPELINE PASS'. Output was: {output}"