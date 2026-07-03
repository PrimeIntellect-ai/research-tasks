# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_pipeline_execution_and_output():
    script_path = "/home/user/pipeline.sh"
    output_path = "/home/user/final_output.txt"

    # Remove the output file if it exists to ensure the script creates it
    if os.path.exists(output_path):
        os.remove(output_path)

    # Execute the pipeline script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed to execute. stderr: {result.stderr}"

    # Check if the output file was created
    assert os.path.isfile(output_path), f"Output file {output_path} was not created by the pipeline script."

    # Verify the contents of the output file
    expected_output = "8,300\n2,235"

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == expected_output, f"Content of {output_path} is incorrect.\nExpected:\n{expected_output}\nGot:\n{content}"