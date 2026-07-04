# test_final_state.py

import os
import subprocess
import pytest

def test_cleaner_cpp_exists():
    assert os.path.isfile("/home/user/cleaner.cpp"), "C++ source file /home/user/cleaner.cpp is missing."

def test_run_pipeline_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Pipeline script {script_path} is not executable."

def test_pipeline_execution_and_output():
    script_path = "/home/user/run_pipeline.sh"
    output_file = "/home/user/clean_data.csv"

    # Remove output file if it exists to ensure the script actually generates it
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the pipeline script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with exit code {result.returncode}. Stderr: {result.stderr}"

    # Check if output file was created
    assert os.path.isfile(output_file), f"Output file {output_file} was not created by the pipeline script."

    # Verify the contents of the output file
    expected_output = (
        "1,45.5,alpha,1\n"
        "3,0.0,delta,0\n"
        "7,10.0,eta,1\n"
        "9,55.5,iota,0\n"
        "10,100.0,kappa,1\n"
    )

    with open(output_file, "r") as f:
        actual_output = f.read()

    assert actual_output.strip() == expected_output.strip(), (
        f"Cleaned data mismatch.\nExpected:\n{expected_output}\nGot:\n{actual_output}"
    )

def test_compiled_executable_exists():
    executable_path = "/home/user/cleaner"
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"Compiled executable {executable_path} is not executable."