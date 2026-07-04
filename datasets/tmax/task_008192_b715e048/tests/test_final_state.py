# test_final_state.py
import os
import subprocess

def test_files_exist_and_executable():
    cpp_file = "/home/user/bayesian_updater.cpp"
    script_file = "/home/user/run_pipeline.sh"

    assert os.path.isfile(cpp_file), f"C++ source {cpp_file} is missing."
    assert os.path.isfile(script_file), f"Bash script {script_file} is missing."
    assert os.access(script_file, os.X_OK), f"Bash script {script_file} is not executable."

def test_pipeline_execution_and_output():
    script_file = "/home/user/run_pipeline.sh"
    output_file = "/home/user/posteriors.csv"

    # Remove output file if it exists to ensure the script creates it fresh
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the pipeline
    result = subprocess.run([script_file], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}. Stderr: {result.stderr}"

    assert os.path.isfile(output_file), f"Output file {output_file} was not created by the pipeline."

    expected_csv = "variant,alpha_post,beta_post\nA,5,7\nB,4,6"

    with open(output_file, "r") as f:
        actual_csv = f.read().strip()

    assert actual_csv == expected_csv, f"Contents of {output_file} do not match expected.\nExpected:\n{expected_csv}\nActual:\n{actual_csv}"