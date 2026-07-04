# test_final_state.py
import os
import subprocess

def test_process_data_cpp_exists():
    assert os.path.isfile('/home/user/process_data.cpp'), "The C++ source file /home/user/process_data.cpp does not exist."

def test_run_pipeline_sh_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_pipeline_execution_and_output():
    script_path = '/home/user/run_pipeline.sh'
    output_path = '/home/user/covariance.txt'
    truth_path = '/tmp/ground_truth_cov.txt'

    # Remove the output file if it exists to ensure the script generates it
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the pipeline
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"The script {script_path} failed to execute properly. Stderr: {result.stderr}"

    assert os.path.isfile(output_path), f"The pipeline did not generate the expected output file at {output_path}."
    assert os.path.isfile(truth_path), f"The ground truth file {truth_path} is missing."

    with open(output_path, 'r') as f:
        output_lines = [line.strip() for line in f.readlines() if line.strip()]

    with open(truth_path, 'r') as f:
        truth_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(output_lines) == len(truth_lines), f"Expected {len(truth_lines)} lines in {output_path}, but found {len(output_lines)}."

    for i, (out_line, truth_line) in enumerate(zip(output_lines, truth_lines)):
        # Split by spaces to handle multiple spaces gracefully
        out_vals = out_line.split()
        truth_vals = truth_line.split()
        assert out_vals == truth_vals, f"Mismatch on line {i+1}. Expected: '{truth_line}', Got: '{out_line}'"