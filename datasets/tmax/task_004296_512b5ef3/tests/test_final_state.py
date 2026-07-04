# test_final_state.py
import os
import subprocess
import pytest

def test_pipeline_files_exist():
    c_file = "/home/user/prepare_data.c"
    sh_file = "/home/user/run_pipeline.sh"

    assert os.path.exists(c_file), f"C program file missing at {c_file}"
    assert os.path.exists(sh_file), f"Shell script missing at {sh_file}"

def test_run_pipeline_and_check_output():
    sh_file = "/home/user/run_pipeline.sh"
    out_file = "/home/user/clean_data.csv"

    # Ensure the script is executable
    os.chmod(sh_file, 0o755)

    # Run the pipeline
    result = subprocess.run([sh_file], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"run_pipeline.sh failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert os.path.exists(out_file), f"Output file {out_file} was not created by the pipeline."

    expected_contents = """user_id,engagement_score,session_duration,bounce_rate,distance
1,0.90,400.00,0.10,100.00
2,0.50,1000.00,0.80,700.00
3,0.40,150.00,0.50,150.00
4,0.80,300.00,0.20,0.00
5,0.50,250.00,0.30,50.00"""

    with open(out_file, "r") as f:
        actual_contents = f.read().strip()

    assert actual_contents == expected_contents, f"Contents of {out_file} do not match the expected output.\nExpected:\n{expected_contents}\nActual:\n{actual_contents}"