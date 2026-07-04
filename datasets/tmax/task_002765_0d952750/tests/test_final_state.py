# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/etl/pipeline.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {script_path} is not executable."

def test_cpp_source_exists():
    cpp_path = "/home/user/etl/graph_solver.cpp"
    assert os.path.isfile(cpp_path), f"C++ source code {cpp_path} does not exist."

def test_pipeline_execution_and_output():
    # Remove output file and executable if they exist to ensure the script creates them
    output_path = "/home/user/output/shortest_path.txt"
    executable_path = "/home/user/etl/graph_solver"

    if os.path.exists(output_path):
        os.remove(output_path)
    if os.path.exists(executable_path):
        os.remove(executable_path)

    # Run the pipeline script
    script_path = "/home/user/etl/pipeline.sh"
    try:
        result = subprocess.run(
            [script_path],
            cwd="/home/user/etl",
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}.\nStderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("Pipeline script execution timed out.")

    # Check if executable was created
    assert os.path.isfile(executable_path), f"Executable {executable_path} was not created by the pipeline script."

    # Check if output file was created
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    # Check output file contents
    with open(output_path, "r") as f:
        actual_content = f.read().strip()

    expected_content = (
        "Length: 4\n"
        "Path: API_Gateway -> Data_Ingestor -> Message_Queue -> Processing_Node -> Storage_Cluster_9"
    )

    assert actual_content == expected_content, (
        f"Output file content does not match expected.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Actual:\n{actual_content}"
    )